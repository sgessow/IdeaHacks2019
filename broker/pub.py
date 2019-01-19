import paho.mqtt.publish as publish

MQTT_SERVER = "172.30.47.196"
MQTT_PATH = "sensor_data"

publish.single(MQTT_PATH, "Hello World!", hostname = "localhost")
