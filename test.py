import requests
import asyncio

async def send(text):
    requests.post('http://127.0.0.1', data={'user': 'root', })

for i in range(30):
