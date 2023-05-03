import serial 
import numpy as np



# Define the Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate


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


# Define the state and action spaces
#states = [get_encoder_value()]  # Encoder states

actions = [-1, 0, 1]  # Motor velocity control

# while True:
#    write_a("OFF")

#    a = 283238*2323

#    write_a("ON\r")
   

print(write_a("ON"))