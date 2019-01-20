import serial
import sys

# Open port
ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.readline())
