import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Create mqttc client
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_text"
message = ""

# Callback when a CONNACK response is received from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_PATH)

# Call back for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    message = str(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(LOCALHOST, 1883, 60)
client.subscribe(MQTT_PATH, 1)

client.loop_forever()

#TODO:
# 1. Properly setup broker such that a publisher can publish a message to the broker (Raspberry Pi) which will then forward it to the server online
# 2. Take a look at javascript implementation to determine what ANDREW FUCKED UP ON GOD DAMMIT
