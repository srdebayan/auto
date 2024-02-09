# data_simulator.py
import paho.mqtt.client as paho
import json
import random
import datetime
import time


# Hostname and port
broker="173.30.0.100"
#broker="172.17.0.2"
port = 1883

def on_publish(client, userdata, result):
    print("Data published.")

# MQTT client setup
client = paho.Client()
client.on_publish = on_publish
client.connect(broker, port)

for i in range(10000):
    imo_number = random.randint(1000, 1500)
    length = random.randint(1, 10)
    width = random.randint(1, 12)
    timestamp = datetime.datetime.now().timestamp()

    data = {
        "IMO_Number": imo_number,
        "Length": length,
        "Width": width,
        "Timestamp": timestamp
    }

    message = json.dumps({"ais_data": data})
    client.publish("ais_data", message)
    print(message)
    time.sleep(5)

#client.disconnect()