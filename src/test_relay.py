import serial
import time

#set up your serial port with the desire COM port and baudrate.
signal = serial.Serial('COM3', baudrate=9600, bytesize=8, stopbits=1, timeout=.1)

#trigger Relay
signal.write("AT+CH1=1".encode())
time.sleep(15)
signal.write("AT+CH1=0".encode())