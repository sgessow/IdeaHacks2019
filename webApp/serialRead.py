import serial
import datetime
import base64
import random
import string
import time
import math
import paho.mqtt.client as paho
import json

SERIAL_PORT = "COM11"
#SERIAL_PORT = input("Serial port of choice: ")

text_channel= 'ideahacks2019_200_accel'
image_channel= 'ideahacks2019_200_images'
broker="broker.hivemq.com"

packet_size=3000
#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

# def convertImageToBase64(image):
#     with open(image, "rb") as image_file:
#         encoded = base64.b64encode(image_file.read())
#         return encoded

def publishEncodedImage(encoded):
	data = encoded.decode('utf-8')
	end = packet_size
	start = 0
	length = len(data)
	picId = 0
	pos = 1
	no_of_packets = math.ceil(length/packet_size)

	while pos <= no_of_packets:
		#data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets}
		dump = {"data": str(data[start:end]), "pic_id":picId, "pos": pos, "size": no_of_packets}
		#print(json.dumps(data))
		client.publish(image_channel, json.dumps(dump))
		#print(encoded[start:end])
		end += packet_size
		start += packet_size
		pos += 1

try:
	print("Opening Serial Port...")
	#initiate serial port to read data from
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=1000000,
	    timeout=3,                         # give up reading after 3 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print("connected to port " + SERIAL_PORT)
except:
	print("<== Error connecting to " + SERIAL_PORT + " ==>")
	exit()

##create plain text file to save raw data as backup for database
# date = str(datetime.datetime.now())
# FILENAME = 'Raw_Data/' + date
# FILENAME = FILENAME.replace(':', '_')
# txtfile = open(FILENAME, "w")
# txtfile.write('Blue Dawn Freq library test starting at ' + date)


client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(text_channel)#subscribe
time.sleep(1)
print("publishing ")
client.publish(text_channel,"yoooo")#publish
time.sleep(1)

print("running")
while ser.isOpen():
	dataString = ser.readline()
	print(dataString)
	dataString = base64.b64encode(dataString)
	publishEncodedImage(dataString)

	# try:
	# 	#get data
	# 	#print('reading...')
	#
	# except:
	# 	print("could not read")
	# 	continue

	# try:
	# 	print('Writing to textfile')
	# 	txtfile.write(dataString)
	# 	txtfile.flush()
	# except:
	# 	pass
