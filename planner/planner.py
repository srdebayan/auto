import paho.mqtt.client as mqtt
import json
import time

# Hostname and port
broker = "173.30.0.100"
port = 1883
publish_topic = "planner_data"
subscribe_topic = "analyzer_data"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(data)
    imo_number = data["IMO_Number"]
    area = data["Area"]

    if 1 <= area <= 40:
        port_assignment = "A"
    elif 41 <= area <= 80:
        port_assignment = "B"
    elif 81 <= area <= 120:
        port_assignment = "C"
    else:
        port_assignment = "Unknown"

    planner_data = {
        "IMO_Number": imo_number,
        "Port": port_assignment
    }

    planner_message = json.dumps(planner_data)
    client.publish("planner_data", planner_message)
    print(planner_data)
    
    # Introduce a 3-second delay
    #time.sleep(3)
    
    
# MQTT client setup
client = mqtt.Client()
client.connect(broker, port)

# Set the callback function for when a message is received
client.on_message = on_message

# Subscribe to the "ais_data" topic
client.subscribe(subscribe_topic)

print("Waiting for AIS data. Press Ctrl+C to exit.")
try:
    # Loop to keep the script running
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting.")
    client.disconnect()