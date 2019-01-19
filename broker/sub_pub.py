from multiprocessing import Pool, Process, Queue
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# MQTT variables
MQTT_SERVER = "broker.mqttdashboard.com"
MQTT_ESP = "sensor_data"
MQTT_BROKER = "ideahacks2019_200_text"

# Global queue to send messages between different threads
queue = Queue()

# MQTT functions
# on_connect is to subscribe to the ESP channel
def on_connect(client, userdata, flags, rc):
    print ("Connected with result code " + str(rc))

    # Subscribe to the ESP
    client.subscribe(MQTT_ESP)

# on_message is to receive the message from the ESP
def on_message(client, userdata, msg):
    print("Received from " + msg.topic + ": " + str(msg.payload))

    # Put test message in new queue for testing
    q2.put("Successfully put some stuff")
    
    # Eventually, the subscriber side of the script will send the received data to the publisher side, using a queue
    queue.put(str(msg.payload))

# Subscriber function will subscribe to the ESPs
def subscriber():
    # Set up MQTT variables
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()

# Publisher function will publish to the server
def publisher(q, q2):
    # Check to see if the queue isn't empty
    while not q.empty():
        # Publish a message to the broker using the data received by the ESP
        publish.single(MQTT_BROKER, q.get(), hostname = MQTT_SERVER)

def test(q):
    # Put test message in new queue for testing
    q.put("Successfully put some stuff")

if __name__ == '__main__':
    print("Initiated subscribe thread")

    # Test queue
    queue2 = Queue()

    # Set up a process to run the publisher side
    p = Process(target=publisher, args=(queue, queue2))
    #p = Process(target=test, args=(queue2,))

    # Start new thread
    p.start()

    # Start subscriber side of the program
    print(queue2.get())
    subscriber()

    # Join thread after running subscriber function?
    p.join()
