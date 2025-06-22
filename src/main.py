import random
import os
import asyncio
import uvicorn
import mqtt_utils

from fastapi import FastAPI
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client


app = FastAPI()

# Shared MQTT client
mqtt_client_instance = None

def save_json(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

async def mqtt_loop():
    mqtt_loop()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, mqtt_client_instance.loop_forever)

# FastAPI route
@app.get("/")
async def read_root():
    return {"message": "FastAPI works!"}

# Startup event to launch MQTT loop
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(mqtt_loop())

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True
    )