import serial 
import numpy as np

def get_encoder_value():
    # Open the serial port
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # Replace 'COM1' with the name of your serial port
    # Wait for the encoder value to be available
    while ser.in_waiting == 0:
        pass
    # Read the encoder value
    encoder_value = ser.readline().decode().strip()
    # Close the serial port
    
    return encoder_value

while True:
    print(get_encoder_value())