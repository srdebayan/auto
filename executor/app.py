from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json
import datetime
import time
 
app = Flask(__name__)
 
# MQTT broker configuration
broker = "173.30.0.100"
port = 1883
subscribe_topic = "planner_data"
publish_topic_executor = "executor_data"
 
# Initialize global variables to store received data
latest_data = {"IMO_Number": "", "Port": ""}
 
 
def on_message(client, userdata, msg):
    global latest_data
    print("41")
 
    data = json.loads(msg.payload)
    #print(data)
    imo_number = data["IMO_Number"]
    port = data["Port"]
    
    latest_data = {"IMO_Number": data.get("IMO_Number", ""), "Port": data.get("Port", "")}
    print(f"Received data: {latest_data}")
    print("42")
    
    exe_data = {
        "IMO_Number": imo_number,
        "Port": port
    }
 
    # Send a message through MQTT to "executor_data" topic
    exe_message = json.dumps(exe_data)
    client.publish(publish_topic_executor, exe_message)
    time.sleep(3)
 
 
# MQTT client setup
client = mqtt.Client()
client.connect(broker, port)
 
#starting the program
#client.publish(publish_topic_executor, "start")
print("43")
 
# Set the callback function for when a message is received
client.on_message = on_message
 
# Subscribe to the "planner_data" topic
client.subscribe(subscribe_topic)
 
 
@app.route("/")
def index():
    return render_template("index.html", data=latest_data)
 
 
if __name__ == "__main__":
    # Loop to keep the script running
    client.loop_start()
    # Run the Flask web application
    app.run(debug=True)