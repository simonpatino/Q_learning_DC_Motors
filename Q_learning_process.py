import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time



# Define the Q-learning parameters

goal= 80   #  velocity neccesary to be succesful 
 
alpha = 0.3 # Learning rate

gamma = 0.9  # Discount factor

epsilon = 0.1  # Exploration rate

#states= list(range(-170,171)) # All posible values sent from the encoder 

states = 255

#actions = [-1, 0, 1] # -1 ----> back , 0 ----> do nothing , ]

#actions = list(range(0,256))

actions = [0,1,2]

q_table= np.zeros((256,3))  #q_table= np.zeros((len(states),len(actions)))

state_actual = 70

goal = 105 #RPM

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # Replace 'COM3' with the appropriate port and 9600 with the baud rate used by your Arduino

a = 0

def epsilon_policy():

    if np.random.uniform(0,1) < epsilon :
        do = np.random.choice(actions)
        #perform action
        if state_actual != 68:
            if do == 0:
                write_a(state_actual +2)
                time.sleep(0.9)
                new_state= state_actual +2

            elif do == 2:
                write_a(state_actual )
                time.sleep(0.9)
                new_state= state_actual 

            else:
                write_a(state_actual -2)  
                time.sleep(0.9)
                new_state= state_actual -2

        else:
            new_state= state_actual + 2

        result= get_encoder_value()
            
    else:

        do = actions[np.argmax(q_table[state_actual])]

        if state_actual != 68:
            if do == 0:
                write_a(state_actual +2)
                time.sleep(0.9)
                new_state= state_actual +2

            elif do == 2:
                write_a(state_actual )
                time.sleep(0.9)
                new_state= state_actual 

            else:
                write_a(state_actual -2)
                time.sleep(0.9)
                new_state= state_actual -2
        else: 
            new_state= state_actual +2 
        #perfom action
        
        
        result= get_encoder_value()
       
    return do, result ,new_state

def get_reward(result):
        
    reward = 1-(abs(goal - result)/150)   #normalizing 
        
    return reward

def get_encoder_value():
  
    puerto_serie = serial.Serial('/dev/cu.usbmodem14101', 9600)
            
    dato = puerto_serie.readline().strip() # leer datos del puerto serie
        
    #puerto_serie.close()
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



def animate(i, dataList,hola):
    #ser.write(b'g')                                     # Transmit the char 'g' to receive the Arduino data point
    #arduinoData_string = ser.readline().decode('ascii') # Decode receive Arduino data as a formatted string
    #print(i)                                           # 'i' is a incrementing variable based upon frames = x argument
    #print(dataList)

    global state_actual
    global goal

    q_table ,do, result , new_state  = q_learning(state_actual)
    
  

    state_actual = new_state 
   
    print(q_table  ,"Accion realizada #:",do,"Velocidad actual (RPM):",result, "Estado actual (0,255):",state_actual )


    dataxd= result

    try:
        #arduinoData_float = float(data)   # Convert to float
        datalist.append(dataxd)              # Add to the list holding the fixed number of points to animate

    except:        
        datalist.append(100)                           # Pass if data point is bad                               
        pass

    dataList = dataList[-50:]                           # Fix the list size so that the animation plot 'window' is x number of points
    
    ax.clear()                                          # Clear last data frame
    ax.plot(dataList)                                   # Plot new data frame
    
    ax.set_ylim([-20, 200])                              # Set Y axis limit of plot
    ax.set_title("Arduino Data")                        # Set title of figure
    ax.set_ylabel("RPM")
    #ax.set_xlabel("Time")
    ax.axhline(y=goal, color='r', linestyle='--')                              # Set title of y axis 


                                   # Create empty list variable for later use
                                                        
fig = plt.figure()                                      # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)                               # Add subplot to main fig window
ax.axhline(y=105, color='r', linestyle='--')
                       # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
                                           # Time delay for Arduino Serial initialization 

                                                        # Matplotlib Animation Fuction that takes takes care of real time plot.
datalist = []                
hola= 1                                              # Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(datalist,hola), interval=100) 

plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
   