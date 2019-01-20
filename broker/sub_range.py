import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_text"

# Rangefinder topic
MQTT_RANGE = "rangefinder_data"

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
        start = s.find("x:")
        end = s.find(",", start)
        acc_x += int(s[start+2:end])

        # Accumulate for y
        start = s.find("y:")
        end = s.find(",", start)
        acc_y += int(s[start+2:end])

        # Accumulate for y
        start = s.find("z:")
        end = s.find(",", start)
        acc_z += int(s[start+2:end])

    # Now average it out with the number of data points
    acc_x /= len(data)
    acc_y /= len(data)
    acc_z /= len(data)

    # Now check to see if the average is bigger than some slop
    if (acc_x > 100 or acc_y > 100 or acc_z > 300):
        return "YOUR ITEM IS BEING STOLEN BITTTCHCHH"
    else:
        return "YOU'RE GOOD DOOGGGGG"

# Callback when a CONNACK response is received from the server
def on_connect_range(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_RANGE)

# Call back for when a PUBLISH message is received from the server
def on_message_range(client, userdata, msg):
    # Global num?
    global num

    # Print message received
    print(msg.topic + " " + str(msg.payload))

    # Local message variable
    message = str(msg.payload)

    # Process the data
    if (num >= 5):
        # Process the message
        final = process(acc_data)

        # Publish to accelerometer topic
        publish.single(MQTT_PATH, final, hostname = MQTT_SERVER)

        # Reset the list
        acc_data[:] = []

        # Reset x
        num = 0
    else:
        # Append the data
        acc_data.append(message)
        num += 1

# Accelerometer Client
client_range = mqtt.Client()
client_range.on_connect = on_connect_range
client_range.on_message = on_message_range
client_range.connect(LOCALHOST, 1883, 60)
client_range.loop_forever()
