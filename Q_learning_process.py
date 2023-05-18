import serial 
import numpy as np
import time

# Define the Q-learning parameters

goal= 100   #  velocity neccesary to be succesful 
 
alpha = 0.8 # Learning rate

gamma = 1  # Discount factor

epsilon = 0.2  # Exploration rate

#states= list(range(-170,171)) # All posible values sent from the encoder 

states = 255

#actions = [-1, 0, 1] # -1 ----> back , 0 ----> do nothing , ]

actions = list(range(0,256))

q_table= np.zeros((1,256))  #q_table= np.zeros((len(states),len(actions)))

state_actual = 0

goal = 80 #RPM

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # Replace 'COM3' with the appropriate port and 9600 with the baud rate used by your Arduino

def epsilon_policy():

    if np.random.uniform(0,1) < epsilon :
        do = np.random.choice(actions)
        #perform action
        write_a(do)
        time.sleep(0.8)
        result= get_encoder_value()
      
    else:
        do = actions[np.argmax(q_table)]
        #perfom action
        write_a(do)
        time.sleep(0.9)
        result= get_encoder_value()
       
    return do, result 

def get_reward(result):
        
        global state_actual
        reward = 1/(goal - result)
        state_actual = result 
        return reward

def get_encoder_value():
  
    puerto_serie = serial.Serial('/dev/cu.usbmodem14101', 9600)
            
    dato = puerto_serie.readline().strip() # leer datos del puerto serie
        
    a= 1
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
     
     do, result = epsilon_policy()
    
     reward = get_reward(result)

     #q_table[state_actual,do] =  q_table[state_actual,do] + alpha*(reward) - (alpha * q_table[state_actual,do]) 

     q_table[0,do] =  q_table[0,do] + alpha*(reward) - (alpha * q_table[0,do]) #+ gamma*alpha*


     return q_table , do
     #new_state = current_state

# while True:
#      #write_a("1")
#      #time.sleep(0.9)
#      print(get_encoder_value())
     
while True:

    tab ,dop= q_learning(state_actual)
    
    #print(state_actual)

    print(tab  ,dop )
     
#get_encoder_value()

