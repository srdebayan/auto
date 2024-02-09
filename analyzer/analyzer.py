import paho.mqtt.client as mqtt
import json
import time

# Hostname and port
broker = "173.30.0.100"
port = 1883
publish_topic = "analyzer_data"
subscribe_topic = "ktoana"



def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(data)
    imo_number = data["IMO_Number"]
    length = data["Length"]
    width = data["Width"]

    area = length * width

    analyzer_data = {
        "IMO_Number": imo_number,
        "Area": area
    }

    analyzer_message = json.dumps(analyzer_data)
    client.publish("analyzer_data", analyzer_message)
    print(analyzer_data)
    # Introduce a 3-second delay
    #time.sleep(1)
    
'''    

def on_message(client, userdata, msg):
    #payload = json.loads(msg.payload)
    data = json.loads(msg.payload)
    print(data)
    
    print("Received AIS data:")
    print("IMO Number:", payload["ais_data"]["IMO_Number"])
    print("Length:", payload["ais_data"]["Length"])
    print("Width:", payload["ais_data"]["Width"])
    print("Timestamp:", payload["ais_data"]["Timestamp"])
    print("--------------------------")
    
'''

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

 




























'''from influxdb import InfluxDBClient

# InfluxDB connection parameters
host = 'localhost'  # Assuming InfluxDB is running on your local machine
port = 8086
database = 'auto'
username = 'admin'
password = 'admin123'

# Create InfluxDB client
#influx_client = InfluxDBClient(host=host, port=port, username=username, password=password)
#influx_client.switch_database(database)

# InfluxDB configuration
influx_url = "http://localhost:8086"
influx_token = "Cqe1sOI_NsKtK1ZpF52QHqd4vHv4SVHwy8SMuYzT9HrKafhT_qtPnotf5XOzVl_B1NQyCy0Np1o9tshGCE1x4w=="  # Replace with your InfluxDB token
influx_org = "univaq"      # Replace with your InfluxDB organization
influx_bucket = "auto"  # Replace with your InfluxDB bucket

# Connect to InfluxDB 2.x
influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
#write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Define data point
measurement = 'your_measurement'
value = 1
tags = {'tag1': 'value1', 'tag2': 'value2'}

# Prepare data
data_point = {
    "measurement": measurement,
    "tags": tags,
    "fields": {"value": value}
}

# Write data point to InfluxDB
influx_client.write_points([data_point])

# Close the connection
influx_client.close()
'''