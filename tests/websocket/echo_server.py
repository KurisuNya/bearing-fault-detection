import asyncio
import sys

sys.path.append(".")
from src.websocket import WebSocket, WebSocketCallback, WebSocketData, WebSocketServer


class EchoCallback(WebSocketCallback):
    async def on_receive(self, websocket: WebSocket, data: WebSocketData):
        print(f"Received: {data}")
        await websocket.send(data)

    async def on_close(self, websocket: WebSocket):
        print(f"Connection closed: {websocket.remote_address}")


if __name__ == "__main__":
    server = WebSocketServer("localhost", 8765, EchoCallback())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.run())
    loop.run_forever()
