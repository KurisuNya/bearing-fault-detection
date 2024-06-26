import asyncio
import sys
import threading

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from .adapter import AdapterFactory
from .clients import Client, ClientManager, ConditionalObserver
from .gui.window import MainWindow
from .websocket import JSONWebSocketCallback, WebSocket, WebSocketData, WebSocketServer


class BearingWebSocketCallback(JSONWebSocketCallback):
    __client_manager: ClientManager

    def __init__(self, client_manager: ClientManager):
        self.__client_manager = client_manager

    async def on_receive(self, websocket: WebSocket, data: WebSocketData):
        json_data = self._parse_json(data)
        if not self.__check_data(json_data):
            raise ValueError("Invalid data format")
        if not self.__client_manager.is_client_exists(hash(websocket)):
            self.__add_client(websocket, json_data)
        else:
            self.__set_client_data(websocket, json_data)

    async def on_close(self, websocket: WebSocket):
        self.__client_manager.remove_client(hash(websocket))

    @staticmethod
    def __check_data(data) -> bool:
        if not isinstance(data, dict):
            return False
        if "device_type" not in data:
            return False
        return True

    def __add_client(self, websocket: WebSocket, data: dict):
        def get_client_name(websocket, data):
            if "device_name" in data:
                return data["device_name"]
            return str(hash(websocket))

        adapter = AdapterFactory.get_adapter(data["device_type"])
        factory = adapter.get_algorithm_factory()

        client_hash = hash(websocket)
        algorithm_data = adapter.get_algorithm_data(data)
        algorithm = factory.get_algorithm(factory.get_algorithm_names()[0])
        new_client = Client(
            client_hash=client_hash,
            client_name=get_client_name(websocket, data),
            algorithm_factory=factory,
            algorithm=algorithm,
            algorithm_index=0,
            algorithm_params=algorithm.get_default_params(),
        )
        self.__client_manager.add_client(client_hash, new_client)
        self.__client_manager.set_client_data(
            client_hash, {"algorithm_data": algorithm_data}
        )

    def __set_client_data(self, websocket: WebSocket, data: dict):
        adapter = AdapterFactory.get_adapter(data["device_type"])
        self.__client_manager.set_client_data(
            hash(websocket), {"algorithm_data": adapter.get_algorithm_data(data)}
        )


class Solver:
    __locks: dict[int, threading.Lock]

    def __init__(self):
        self.__locks = {}

    def solve(self, client: Client):
        thread = threading.Thread(target=self.__run, args=(client,))
        thread.start()

    def __run(self, client: Client):
        lock = self.__get_lock(client.client_hash)
        with lock:
            client.algorithm.solve(
                data=client.algorithm_data,
                params=client.algorithm_params,
            )

    def __get_lock(self, client_hash: int):
        if client_hash not in self.__locks:
            self.__locks[client_hash] = threading.Lock()
        return self.__locks[client_hash]


class App:

    @staticmethod
    async def websocket_run(path: str, port: int):
        solver = Solver()
        algorithm_observer = ConditionalObserver(
            lambda _, k: k == "algorithm"
            or k == "algorithm_data"
            or k == "algorithm_params",
            lambda client, _: solver.solve(client),
        )

        client_manager = ClientManager(client_observers=[algorithm_observer])
        callback = BearingWebSocketCallback(client_manager)
        server = WebSocketServer(path, port, callback)
        await server.run()

    @staticmethod
    def run(path: str, port: int):
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()

        event_loop = QEventLoop(app)
        asyncio.set_event_loop(event_loop)
        app_close_event = asyncio.Event()
        app.aboutToQuit.connect(app_close_event.set)
        event_loop.create_task(App.websocket_run(path, port))
        event_loop.run_until_complete(app_close_event.wait())
        event_loop.close()
