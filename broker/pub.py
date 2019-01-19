import paho.mqtt.publish as publish
import sys

MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PATH = "ideahacks2019_200_text"

while True:
    message = sys.stdin.readline()
    publish.single(MQTT_PATH, message, hostname = MQTT_SERVER)
