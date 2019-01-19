import paho.mqtt.publish as publish

MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_PATH = "ideahacks2019_200_text"

publish.single(MQTT_PATH, "Hello World!", hostname = MQTT_SERVER)
