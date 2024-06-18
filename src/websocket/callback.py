from abc import ABCMeta, abstractmethod
import json

from websockets import Data as WebSocketData, WebSocketServerProtocol as WebSocket


class WebSocketCallback(metaclass=ABCMeta):
    @abstractmethod
    async def on_receive(self, websocket: WebSocket, data: WebSocketData):
        pass

    @abstractmethod
    async def on_close(self, websocket: WebSocket):
        pass


class JSONWebSocketCallback(WebSocketCallback):
    @abstractmethod
    async def on_receive(self, websocket: WebSocket, data: WebSocketData):
        pass

    @abstractmethod
    async def on_close(self, websocket: WebSocket):
        pass

    @staticmethod
    def _parse_json(data: WebSocketData):
        if isinstance(data, str):
            return json.loads(data)
        raise ValueError("Data is not a string")
