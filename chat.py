import asyncio
import logging
import websockets
import json
from websockets import WebSocketServerProtocol

logging.basicConfig()
messages = open('chat.txt', 'w+')


USERS = set()
async def send_message(message):
        logging.error(message)
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def counter(websocket, path):
    global messages
    await register(websocket)
    logging.error('edfhjuweif')
    try:
        async for message in websocket:
            data = str(message)
            save_data = json.loads(data)
            messages.write(messages.read() + save_data['login'] + ':' + save_data['text'] + '\n')
            await send_message(data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "127.0.0.1", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()