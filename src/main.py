import random
import os
import asyncio
import uvicorn
import mqtt_utils as mqtt_utils

from fastapi import FastAPI

app = FastAPI()

mqtt_client_instance = mqtt_utils.connect_mqtt()
mqtt_utils.subscribe(mqtt_client_instance)

@app.on_event("startup")
def startup_event():
    mqtt_utils.loop_mqtt()
    print("MQTT client started")

# FastAPI route
@app.get("/")
async def read_root():
    return {"message": "FastAPI works!"}

def run_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True
    )

if __name__ == "__main__":
    run_server()
