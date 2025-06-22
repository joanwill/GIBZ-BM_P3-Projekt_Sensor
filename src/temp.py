import random
import os
import uvicorn
import threading

from fastapi import FastAPI
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

app = FastAPI()

# load .env file with credentials
load_dotenv()

# variables for mqtt
mqtt_broker = "eu2.cloud.thethings.industries"
mqtt_port = 1883
mqtt_topic = "v3/haus@vebl-network/devices/eui-a81758fffe07a941/up"
mqtt_id = f'subscribe{random.randint(0, 100)}'
mqtt_username = "haus@vebl-network"
mqtt_password = os.getenv('MQTT_PW')

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client

def save_json(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        save_json("raw.json", msg.payload.decode())
    client.subscribe(mqtt_topic)
    client.on_message = on_message

async def mqtt_start():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

# FastAPI
@app.get("/")
def read_root():
    return {"message": "FastAPI works!"}

def running_server():
    try:
        # Create and start mqtt thread
        #mqtt_thread = threading.Thread(target=mqtt_start)
        #mqtt_thread.start()

        # Start API webserver
        uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
    except Exception as e:
        print(f"Crashed: {e}")
    finally:
        print("Shutting down the server gracefully...")
        mqtt_thread.do_run = False
        print("Done!")

# Main
if __name__ == "__main__":
    running_server()