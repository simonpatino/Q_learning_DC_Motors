
#PRUEBA DESTRUCIVA 

import serial 
import numpy as np
import time

# Define the Q-learning parameters

goal= 100   #  velocity neccesary to be succesful 
 
alpha = 0.85 # Learning rate

gamma = 0.95  # Discount factor

epsilon = 0.1  # Exploration rate

#states= list(range(-170,171)) # All posible values sent from the encoder 

states = 255

#actions = [-1, 0, 1] # -1 ----> back , 0 ----> do nothing , ]

#actions = list(range(0,256))

actions = [0,1]

q_table= np.zeros((256,2))  #q_table= np.zeros((len(states),len(actions)))

state_actual = 70

goal = 105 #RPM

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # Replace 'COM3' with the appropriate port and 9600 with the baud rate used by your Arduino

a = 0

def epsilon_policy():

    if np.random.uniform(0,1) < epsilon :
        do = np.random.choice(actions)
        #perform action
        if state_actual != 69:
            if do == 0:
                write_a(state_actual +1)
                time.sleep(0.9)
                new_state= state_actual +1
            else:
                write_a(state_actual -1)  
                time.sleep(0.9)
                new_state= state_actual -1

        else:
            new_state= state_actual + 1

        result= get_encoder_value()
            
    else:

        do = actions[np.argmax(q_table[state_actual])]

        if state_actual != 69:
            if do == 0:
                write_a(state_actual +1)
                time.sleep(0.9)
                new_state= state_actual +1
            else:
                write_a(state_actual -1)
                time.sleep(0.9)
                new_state= state_actual -1
        else: 
            new_state= state_actual +1 
        #perfom action
        
        
        result= get_encoder_value()
       
    return do, result ,new_state

def get_reward(result):
        
    reward = -abs(goal - result)  
        
    return reward

def get_encoder_value():
  
    puerto_serie = serial.Serial('/dev/cu.usbmodem14101', 9600)
            
    dato = puerto_serie.readline().strip() # leer datos del puerto serie
        
    global a

    try:
        a = (int(float(dato.decode("latin1"))))
        
    except ValueError:
         None
    return  a 
    
def write_a(number):

    #ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # Replace 'COM3' with the appropriate port and 9600 with the baud rate used by your Arduino
    # Wait for the Arduino to initialize
    time.sleep(0.8)

    # Send messages to Arduino
    messages = [str(number)+"\r"]
    for message in messages:
        ser.write(message.encode())
        ser.write(b'\n')  # Add a newline character as a delimiter (optional)
        time.sleep(0.3)  # Delay between sending messages

    # Close the serial port
    #ser.close()
    
def q_learning(evaluar):
     
     do, result, new_state = epsilon_policy()
    
     reward = get_reward(result)

     #q_table[state_actual,do] =  q_table[state_actual,do] + alpha*(reward) - (alpha * q_table[state_actual,do]) 

     q_table[state_actual,do] =  q_table[state_actual,do] + alpha*(reward) - (alpha * q_table[state_actual,do]) + gamma*alpha*np.max(q_table[new_state])

     
     
     
     return q_table , do , result , new_state
     #new_state = current_state

# while True:
#      #write_a("1")
#      #time.sleep(0.9)
#      print(get_encoder_value())
     
while True:

    q_table ,do, result , new_state  = q_learning(state_actual)
    
    state_actual = new_state 
   

   


    print(q_table  ,do,result, state_actual )
    
    #print(get_encoder_value())
#

