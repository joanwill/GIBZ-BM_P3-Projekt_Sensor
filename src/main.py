import random
import os

from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    client.subscribe(mqtt_topic)
    client.on_message = on_message

if __name__ == "__main__":
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
