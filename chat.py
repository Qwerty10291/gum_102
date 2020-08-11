import asyncio
import logging
import websockets
import json

class Chat:
    async def __init__(self):
        self.clients = set()

    async def register(self, ws):
        await self.clients.add(ws)
    
    async def unregister(self, ws):
        await self.clients.remove(ws)
    
    async def send_message(self, message):
        await asyncio.wait([client.send_message() for client in self.clients])
    
    async def message_handler(self, ws, path):
        self.register(ws)
        try:
            async for message in ws:
                self.send_message(message)
        finally:
            self.unregister(ws)