#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import requests
import json

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

# async def generateMessage(websocket):

# async def send(websocket, message):
#     try:
#         await websocket.send(message)
#     except websockets.ConnectionClosed:
#         pass
#             ...
#             for websocket in CLIENTS:
#                 asyncio.create_task(send(websocket, message))
#             ...

async def hello(websocket, path):

    # CLIENTS.add(websocket)
    
    name = await websocket.recv()
    print(f"< {name}")
    greeting = f"Hello {name}!"

    await register(websocket, greeting)

    try:
        async for greeting in websocket:
        # async for message in websocket:
        # await websocket.send(greeting)
            await asyncio.wait([client.send(greeting) for client in CLIENTS])
        # await websocket.send(state_event())
    finally:
        print("killing connection")
        CLIENTS.remove(websocket)

    # name = await generateMessage(websocket)
    # MESSAGES.append(greeting)

    
    # MESSAGES.clear()

    # async for message in websocket:
    #     await register(websocket, greeting)


    # await asyncio.wait([client.send(greeting) for client in CLIENTS])

    #print(f"> {greeting}")
    # await asyncio.sleep(1)

start_server = websockets.serve(hello, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
