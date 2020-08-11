from chat import Chat as cht
import websockets
import asyncio
server = cht()
start_server = websockets.serve(server.message_handler, "127.0.0.1", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()