import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_text"

# Rangefinder topic
MQTT_RANGE = "rangefinder_data"

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

    # Publish to range topic
    publish.single(MQTT_PATH, message, hostname = MQTT_SERVER)

# Accelerometer Client
client_range = mqtt.Client()
client_range.on_connect = on_connect_range
client_range.on_message = on_message_range
client_range.connect(LOCALHOST, 1883, 60)
client_range.loop_forever()
