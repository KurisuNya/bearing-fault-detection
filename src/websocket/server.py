import asyncio

import websockets
from websockets import WebSocketServerProtocol as WebSocket
from .callback import WebSocketCallback


class WebSocketServer:
    __path: str
    __port: int

    def __init__(self, path: str, port: int, callback: WebSocketCallback):
        self.__path = path
        self.__port = port
        self.__callback = callback

    async def run(self):
        async with websockets.serve(self.__handler, self.__path, self.__port):
            await asyncio.Future()

    async def __handler(self, websocket: WebSocket):
        while True:
            try:
                message = await websocket.recv()
            except websockets.ConnectionClosed:
                await self.__callback.on_close(websocket)
                break
            await self.__callback.on_receive(websocket, message)
