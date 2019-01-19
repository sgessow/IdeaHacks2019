import paho.mqtt.publish as publish

MQTT_SERVER = "172.30.47.196"
MQTT_PATH = "ideahacks2019_200_text"

publish.single(MQTT_PATH, "Hello World!", hostname = MQTT_SERVER)
