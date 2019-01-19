import base64, random, string
import time
import paho.mqtt.client as paho

broker="broker.hivemq.com"
broker="iot.eclipse.org"

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("house/bulb1")#subscribe
time.sleep(2)
print("publishing ")
client.publish("house/bulb1","on")#publish
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop


def convertImageToBase64():
 with open("image_test.jpg", "rb") as image_file:
 encoded = base64.b64encode(image_file.read())
 return encoded

def randomword(length):
 return ''.join(random.choice(string.lowercase) for i in range(length))

def publishEncodedImage(encoded):

 end = packet_size
 start = 0
 length = len(encoded)
 picId = randomword(8)
 pos = 0
 no_of_packets = math.ceil(length/packet_size)


 while start <= len(encoded):
 data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets}
 client.publishEvent("Image-Data",json.JSONEncoder().encode(data))
 end += packet_size
 start += packet_size
 pos = pos +1
