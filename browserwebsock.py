#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import requests

def state_event():
    return json.dumps({"type": "state", **"hello"})
    
async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")
    greeting = f"Hello {name}!"
    print(f"> {greeting}")

    async for message in websocket:    
        message = state_event();
        # name = await websocket.recv()

        await websocket.send(message)
        # await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(hello, "127.0.0.1", 5678)

# asyncio.get_event_loop().run_in_executor(None,hello)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()