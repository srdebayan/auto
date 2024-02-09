#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:52:23 2024

@author: debayanb
"""

import paho.mqtt.client as mqtt
import json


# Hostname and port
broker = "173.30.0.100"
port = 1883
topic = "ais_data"




def on_publish(client, userdata, result):
    print("Data published.")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    #print(data)

    ais_data = data.get('ais_data', {})  # Extract 'ais_data' dictionary
    imo_number = ais_data.get('IMO_Number')
    length = ais_data.get('Length')
    width = ais_data.get('Width')
    timestamp = ais_data.get('Timestamp')


    

    if 1 <= length <= 15 and 1 <= width <= 15:
        monitor_data = {
            "IMO_Number": imo_number,
            "Length": length,
            "Width": width,
            "Timestamp": timestamp
        }
        monitor_message = json.dumps(monitor_data)

        client.publish("monitor_data", monitor_message)


# MQTT client setup
client = mqtt.Client()
client.connect(broker, port)

# Set the callback function for when a message is received


client.on_message = on_message

client.on_publish = on_publish

# Subscribe to the "simulator" topic
client.subscribe(topic)

print("Waiting for data. Press Ctrl+C to exit.")
try:
    # Loop to keep the script running
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting.")
    client.disconnect()
