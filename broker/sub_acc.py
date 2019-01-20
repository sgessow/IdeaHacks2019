import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys

# Create general variables
MQTT_SERVER = "broker.mqttdashboard.com"
LOCALHOST = "localhost"
MQTT_PATH = "ideahacks2019_200_accel"

# Accelerometer topic
MQTT_ACC = "accelerometer_data"

# List of values
acc_data = []

# Max number of stuff
num = 0

# Baseline numbers
base = 0
max_base = 10
base_x = 0
base_y = 0
base_z = 0

# Process data function
def process(data):
    # Set global variables
    global base, max_base, base_x, base_y, base_z

    # Accumulators for the different fields
    acc_x = 0
    acc_y = 0
    acc_z = 0

    # loop through the couple of values in the list
    for s in data:
        # Accumulate for x
        start = s.find("x:")
        end = s.find(",", start)
        if (base < max_base):
            base_x += int(s[start+2:end])
        else:
            acc_x += int(s[start+2:end])

        # Accumulate for y
        start = s.find("y:")
        end = s.find(",", start)
        if (base < max_base):
            base_y += int(s[start+2:end])
        else:
            acc_y += int(s[start+2:end])

        # Accumulate for y
        start = s.find("z:")
        end = s.find(",", start)
        if (base < max_base):
            base_z += int(s[start+2:end])
        else:
            acc_z += int(s[start+2:end])

    # Now average it out with the number of data points
    if (base > max_base):
        acc_x /= len(data)
        acc_y /= len(data)
        acc_z /= len(data)

    # Now check to see if the average is bigger than some slop
    if (base > max_base):
        if (abs(base_x - acc_x) > 20 or abs(base_y - acc_y) > 20 or abs(base_z - acc_z) > 20):
            return 1
        else:
            return 0

# Callback when a CONNACK response is received from the server
def on_connect_acc(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Type of subcribing allows for reconnection on termination of signal
    client.subscribe(MQTT_ACC)

# Call back for when a PUBLISH message is received from the server
def on_message_acc(client, userdata, msg):
    # Global num?
    global num, base, max_base, base_x, base_y, base_z

    # Print message received (for shits and giggles)
    print(msg.topic + " " + str(msg.payload))

    # Local message variable
    message = str(msg.payload)

    # Establish baseline
    if (base < max_base):
        # Append data
        acc_data.append(message)

        # Call process
        process(acc_data)

        # Reset data
        acc_data[:] = []
    elif (base == max_base):
        base_x /= max_base
        base_y /= max_base
        base_z /= max_base
    else:
        # Now normal loop
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

    # Increase base
    base += 1
    
# Accelerometer Client
client_acc = mqtt.Client()
client_acc.on_connect = on_connect_acc
client_acc.on_message = on_message_acc
client_acc.connect(LOCALHOST, 1883, 60)
client_acc.loop_forever()
