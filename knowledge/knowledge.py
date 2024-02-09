import paho.mqtt.client as mqtt
import json
import pandas as pd
from time import sleep
import datetime


# MQTT broker configuration
broker = "173.30.0.100"
port = 1883
monitor_topic = "monitor_data"
executor_topic = "executor_data"
publish_topic_ktoana = "ktoana"

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["IMO_Number", "Length", "Width", "Timestamp"])
df2 = pd.DataFrame(columns=["IMO_Number", "Length", "Width", "Timestamp"])
df3 = pd.DataFrame(columns=["Timestamp", "IMO_Number", "Port"])

def on_monitor_data(client, userdata, msg):
    global df
    global df2

    data = json.loads(msg.payload)
    
    imo_number = data.get('IMO_Number')
    length = data.get('Length')
    width = data.get('Width')
    timestamp = data.get('Timestamp')

    # Append the new data to the DataFrame
    new_row = {'IMO_Number': imo_number, 'Length': length, 'Width': width, 'Timestamp': timestamp}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df2 = df
    print("monitordf")
    print(df.head(5))
    print("Received and added data to DataFrame:")
    #print(df)
    if not df.empty:
        print("12")

        print("14")
        #print("Deleted row with the oldest timestamp:")
        #print("exe_df")
        #print(df.head(5))
        #print(df)
        # Get the data with the oldest timestamp
        oldest_data = df[df['Timestamp'] == df['Timestamp'].min()][["IMO_Number", "Length", "Width"]].to_dict('records')[0]
        print("15")
        # Publish the data to the "ktoana" topic
        executor_client.publish(publish_topic_ktoana, json.dumps(oldest_data))
        print(f"Published data with the oldest timestamp to '{publish_topic_ktoana}': {oldest_data}")
        oldest_timestamp = df['Timestamp'].min()
        print("13")
        df = df[df['Timestamp'] != oldest_timestamp]
        print("16")

    else:
        print("DataFrame is empty, cannot delete.")
    
    
    
def on_executor_data(client, userdata, msg):
    global df3

    data = json.loads(msg.payload.decode('utf-8'))
    print(f"Received data from 'executor_data' topic: {data}")

    # Extract relevant data from the received JSON and create a new DataFrame row
    new_data = {"Timestamp": pd.Timestamp.now(), "IMO_Number": data['IMO_Number'], "Port": data['Port']}

    # Append the new data to the DataFrame
    #df3 = df3.append(new_data, ignore_index=True)
    #new_row2 = {'Timestamp': imo_number, 'Length': length, 'Width': width, 'Timestamp': timestamp}
    df3 = pd.concat([df3, pd.DataFrame([new_data])], ignore_index=True)

    print("Updated DataFrame:")
    print(df3.head())
            
    '''        
     # to start the program 
    if "start" in executor_data:
        print("17")
        # Wait for 3 seconds
        sleep(3)
        print("18")
        # Get the data with the oldest timestamp
        #print("haleluah")
        #print(df)
        oldest_data = df[df['Timestamp'] == df['Timestamp'].min()][["IMO_Number", "Length", "Width"]].to_dict('records')[0]
        print("19")
        #print("test1111")
        # Publish the data to the "ktoana" topic
        executor_client.publish(publish_topic_ktoana, json.dumps(oldest_data))
        print(f"Published data with the oldest timestamp to '{publish_topic_ktoana}': {oldest_data}")
        
       ''' 
        
        
            
'''            
def on_executor_data(client, userdata, msg):
    global df

    executor_data = msg.payload.decode('utf-8')
    print(f"Received data from 'executor_data' topic: {executor_data}")

    # Check if the message contains "send next"
    if "send next" in executor_data:
        # Wait for 3 seconds
        sleep(3)

        # Delete the row with the oldest timestamp
        if not df.empty:
            oldest_timestamp = df['Timestamp'].min()
            df = df[df['Timestamp'] != oldest_timestamp]
            print("Deleted row with the oldest timestamp:")
            #print(df)

            # Get the data with the oldest timestamp
            oldest_data = df[df['Timestamp'] == df['Timestamp'].min()][["IMO_Number", "Length", "Width"]].to_dict('records')[0]

            # Publish the data to the "ktoana" topic
            executor_client.publish(publish_topic_ktoana, json.dumps(oldest_data))
            print(f"Published data with the oldest timestamp to '{publish_topic_ktoana}': {oldest_data}")
        else:
            print("DataFrame is empty, cannot delete.")
'''

# MQTT client setup for monitor data
monitor_client = mqtt.Client()
monitor_client.on_message = on_monitor_data
monitor_client.connect(broker, port)
monitor_client.subscribe(monitor_topic)

# MQTT client setup for executor data
executor_client = mqtt.Client()
executor_client.on_message = on_executor_data
executor_client.connect(broker, port)
executor_client.subscribe(executor_topic)

'''
# Publish the test dummy data to "ktoana" topic
test_dummy_data = {
    "IMO_Number": 9999,
    "Length": 5,
    "Width": 5,
    "Timestamp": datetime.datetime.now().timestamp()
}
executor_client.publish(publish_topic_ktoana, json.dumps(test_dummy_data))
print(f"Published test dummy data to '{publish_topic_ktoana}': {test_dummy_data}")
'''

print("Waiting for data. Press Ctrl+C to exit.")
try:
    # Loop to keep the script running for each client
    monitor_client.loop_start()
    executor_client.loop_start()
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting.")
    monitor_client.disconnect()
    executor_client.disconnect()
