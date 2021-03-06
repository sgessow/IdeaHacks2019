import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_rangefinder"

# Rangefinder topic
MQTT_RANGE = "rangefinder_data"

# Global num
num = 0

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
        return 1
    else:
        return 0

# Callback when a CONNACK response is received from the server
def on_connect_range(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_RANGE)

# Call back for when a PUBLISH message is received from the server
def on_message_range(client, userdata, msg):
    global num
    # Print message received
    #print(msg.topic + " " + str(msg.payload))

    # Local message variable
    message = str(msg.payload)

    # Process data
    final = process(message)

    if (final == 1 or num >= 20):
        # Publish the message
        publish.single(MQTT_PATH, final, hostname = MQTT_SERVER)
        num = 0
    else:
        num += 1

# Accelerometer Client
client_range = mqtt.Client()
client_range.on_connect = on_connect_range
client_range.on_message = on_message_range
client_range.connect(LOCALHOST, 1883, 60)
client_range.loop_forever()
