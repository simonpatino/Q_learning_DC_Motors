import serial 
import numpy as np

# Define the Q-learning parameters

goal= 100   #  velocity neccesary to be succesful 
 
alpha = 0.1  # Learning rate

gamma = 0.9  # Discount factor

epsilon = 0.1  # Exploration rate

states= list(range(-170,171)) # All posible values sent from the encoder 
    
actions = [-1, 0, 1] # -1 ----> back , 0 ----> do nothing , ]

q_table= np.zeros((len(states),len(actions)))

state_actual=0

def epsilon_policy(state_actual):

    if np.random.uniform(0,1) < epsilon :
        do = np.random.choice(actions)
        #perform action
        write_a(do)
        result= get_encoder_value()
      
    else:
        do = actions[np.argmax(q_table[state_actual])]
        #perfom action
        write_a(do)
        result= get_encoder_value()
       

    return do, result

def get_reward(result):
        #reward_table= np.zeros((len(states),len(actions)))
        reward = 100*(result/goal)
        #reward_table[state_actual,do]= reward

        return reward

    
def get_encoder_value():
    # Open the serial port
    ser = serial.Serial('/dev/cu.usbmodem14101', 115200)  # Replace 'COM1' with the name of your serial port
    # Wait for the encoder value to be available
    while ser.in_waiting == 0:
        pass
    # Read the encoder value
    encoder_value = ser.readline().decode().strip()
    # Close the serial port
    ser.close()

    return encoder_value

def write_a(number):
    ser = serial.Serial('/dev/cu.usbmodem14101',  9600)  
    message = str(number)+"\r"
    message = str(number).encode() 
    ser.write(message)
    ser.close()
    return message

def q_learning(reward):
     
     
     do, result = epsilon_policy(state_actual)
     reward = get_reward()

     q_table[state_actual,do] =  q_table[state_actual,do] + alpha*(reward) - (alpha * q_table[state_actual,do]) 
     #new_state = current_state

# Define the state and action spaces
#states = [get_encoder_value()]  # Encoder states

 # Motor velocity control

# while True:
#    write_a("OFF")

#    a = 283238*2323

#    write_a("ON\r")
   

print(write_a("ON"))