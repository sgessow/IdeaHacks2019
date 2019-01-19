import paho.mqtt.publish as publish

LOCALHOST = "localhost"
MQTT_ESP = "rangefinder_data"

publish.single(MQTT_ESP, "Fuck you MQTT!", hostname = LOCALHOST)
