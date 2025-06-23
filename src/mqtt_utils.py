import os
import random
import asyncio

from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

# Load .env file with credentials
load_dotenv()

# MQTT connection details
mqtt_broker = "eu2.cloud.thethings.industries"
mqtt_port = 1883
mqtt_topic = "v3/haus@vebl-network/devices/eui-a81758fffe07a941/up"
mqtt_id = f'subscribe{random.randint(0, 100)}'
mqtt_username = "haus@vebl-network"
mqtt_password = os.getenv('MQTT_PW')

def save_json(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def connect_mqtt() -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt_client.Client(mqtt_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    return client

def subscribe(client: mqtt_client.Client):
    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}'")
        save_json("raw.json", msg.payload.decode())
    
    def on_subscribe(client, userdata, mid, granted_qos):
        print(f"✅ Subscribed to {mqtt_topic} with QoS {granted_qos}")

    client.subscribe(mqtt_topic)
    client.on_subscribe = on_subscribe
    client.on_message = on_message

def loop_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.connect(mqtt_broker, mqtt_port)
    client.loop_start()