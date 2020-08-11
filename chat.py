import asyncio
import logging
import websockets
import json
logging.basicConfig(level=logging.INFO)

class Chat:
    clients = set()

    async def register(self, websocket):
        self.clients.add(websocket)
        logging.info(f'r{websocket}')

    
    async def unregister(self, websocket):
        logging.info(f'q{websocket}')
        self.clients.remove(websocket)

    
    async def send_message(self, message):
        await asyncio.wait([client.send_message(message) for client in self.clients])
        logging.info(message)
    
    async def message_handler(self, ws, path):
        logging.info(f'hand{ws}')
        await self.register(ws)
        try:
            async for message in ws:
                self.send_message(message)
        finally:
            self.unregister(ws)