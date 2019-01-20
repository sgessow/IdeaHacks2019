import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial
import sys

# Open port
ser = serial.Serial('/dev/ttyUSB0', 115200)
sys.stdout = open('file.RAW', 'w')
print(ser.readline())
sys.stdout.close()

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_text"

# Rangefinder topic
MQTT_RANGE = "rangefinder_data"

# Process data function
def process(data):
    # Accumulators for the different fields
    distance = 0

    # Accumulate for x
    start = data.find("distance:")
    end = data.find("}", start)
    distance = float(data[start+9:end])

    # Now check to see if the average is bigger than some slop
    if (distance < 50):
        return "YOUR ITEM IS BEING STOLEN BITTTCHCHH"
    else:
        return "YOU'RE GOOD DOOGGGGG"

# Callback when a CONNACK response is received from the server
def on_connect_range(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_RANGE)

# Call back for when a PUBLISH message is received from the server
def on_message_range(client, userdata, msg):
    # Print message received
    print(msg.topic + " " + str(msg.payload))

    # Local message variable
    message = str(msg.payload)

    # Process data
    final = process(message)

    # Publish the message
    publish.single(MQTT_PATH, final, hostname = MQTT_SERVER)

# Accelerometer Client
client_range = mqtt.Client()
client_range.on_connect = on_connect_range
client_range.on_message = on_message_range
client_range.connect(LOCALHOST, 1883, 60)
client_range.loop_forever()
