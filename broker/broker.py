import paho.mqtt.client as mqtt

# Create mqttc client
MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PATH = "ideahacks2019_200_text"

# Callback when a CONNACK response is received from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_PATH)

# Call back for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
