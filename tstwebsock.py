#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import requests
import json

# import cv2
# import mss
# import numpy

CLIENTS = set()
MESSAGES = []

def client_event(greeting):
    # return json.dumps({"type": "client", "count": len(CLIENTS)})
    return json.dumps(greeting)

async def notify_clients(greeting):
    if CLIENTS:  # asyncio.wait doesn't accept an empty list
        message = client_event(greeting)
        await asyncio.wait([client.send(message) for client in CLIENTS])

async def register(websocket, greeting):
    CLIENTS.add(websocket)
    await notify_clients(greeting)

async def notify(message):
    if CLIENTS:  # asyncio.wait doesn't accept an empty list
        toDeliver = message;
        await asyncio.wait([client.send(toDeliver) for client in CLIENTS])
    
async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


async def goodbye(websocket, path):

    CLIENTS.add(websocket)
    
    print(len(CLIENTS))
    print("IT IS WORKING!!")
    dumbassBool = True;

    try:
        while dumbassBool:

            signal = await websocket.recv()

            if signal == "new connection":
                await asyncio.wait([client.send(json.dumps({"type": "new connection", "count": len(CLIENTS)})) for client in CLIENTS])
            else:
                await asyncio.wait([client.send((signal)) for client in CLIENTS])
            
            print(len(CLIENTS))
            print(signal)

    finally:
        dumbassBool = False;
        print("killing connection")
        CLIENTS.remove(websocket)

start_server = websockets.serve(goodbye, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
