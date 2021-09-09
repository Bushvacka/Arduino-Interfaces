#Troy Dutton
#Logs data from Arduino's Serial Moniter
import serial#Importing serial to read data from the arduino
import time#Importing time to have a time stamp with the data

#Debugging
#import serial.tools.list_ports
#for comport in serial.tools.list_ports.comports():
#    print(comport.device)

ser = serial.Serial("COM5", 9600)#Create a serial object

while True:
    ser_bytes = ser.readline()
    decoded_byte = ser_bytes[0:len(ser_bytes)].decode("utf-8").strip("\n").strip("\r")
    print(decoded_byte)