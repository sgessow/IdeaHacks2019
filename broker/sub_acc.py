import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_text"

# Accelerometer topic
MQTT_ACC = "accelerometer_data"

# List of values
acc_data = []

# Max number of stuff
num = 0

# Process data function
def process(data):
    # Accumulators for the different fields
    acc_x = 0
    acc_y = 0
    acc_z = 0

    # loop through the couple of values in the list
    for s in data:
        # Accumulate for x
        start = s.rfind("x:")
        end = s.rfind(",", start)
        acc_x += int(s[start:end])

        # Accumulate for y
        start = s.rfind("y:")
        end = s.rfind(",", start)
        acc_x += int(s[start:end])

        # Accumulate for y
        start = s.rfind("z:")
        end = s.rfind(",", start)
        acc_x += int(s[start:end])

    # Now average it out with the number of data points
    acc_x /= len(s)
    acc_y /= len(s)
    acc_z /= len(s)

    # Now check to see if the average is bigger than some slop
    if (acc_x > 100 or acc_y > 100 or acc_y > 100):
        return "YOUR ITEM IS BEING STOLEN BITTTCHCHH"
    else:
        return "YOU'RE GOOD DOOGGGGG"

# Callback when a CONNACK response is received from the server
def on_connect_acc(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_ACC)

# Call back for when a PUBLISH message is received from the server
def on_message_acc(client, userdata, msg):
    # Global num?
    global num

    # Print message received (for shits and giggles)
    print(msg.topic + " " + str(msg.payload))

    # Local message variable
    message = str(msg.payload)

    # Process the data
    if (num >= 5):
        # Process the message
        final = process(acc_data)
        print(num)
        # Publish to accelerometer topic
        publish.single(MQTT_PATH, final, hostname = MQTT_SERVER)

        # Reset the list
        acc_data[:] = []

        # Reset x
        num = 0
    else:
        num += 1
    
# Accelerometer Client
client_acc = mqtt.Client()
client_acc.on_connect = on_connect_acc
client_acc.on_message = on_message_acc
client_acc.connect(LOCALHOST, 1883, 60)
client_acc.loop_forever()
