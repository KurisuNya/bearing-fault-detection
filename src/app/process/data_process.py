import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from threading import Lock
from typing import Any, Callable

from ...adapter import AdapterFactory
from ...algorithm import AlgorithmResult
from ...clients import (
    Client,
    ClientExistError,
    ClientManager,
    ConditionalObserver,
    MessageManager,
)
from ...websocket import (
    JSONWebSocketCallback,
    WebSocket,
    WebSocketData,
    WebSocketServer,
)
from ..utils import AsyncConnection, AsyncQueue, FuncData


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
        algorithm_name = factory.get_algorithm_names()[0]
        algorithm = factory.get_algorithm(algorithm_name)
        new_client = Client(
            client_id=client_hash,
            client_name=get_client_name(websocket, data),
            algorithm_factory=factory,
            algorithm=algorithm,
            algorithm_name=algorithm_name,
            algorithm_params=algorithm.get_default_params(),
        )
        self.__client_manager.add_client(new_client)
        self.__client_manager.set_client_data(
            client_hash, {"algorithm_data": algorithm_data}
        )

    def __set_client_data(self, websocket: WebSocket, data: dict):
        adapter = AdapterFactory.get_adapter(data["device_type"])
        self.__client_manager.set_client_data(
            hash(websocket), {"algorithm_data": adapter.get_algorithm_data(data)}
        )


class AlgorithmSolver:
    __pool: ThreadPoolExecutor
    __locks: dict[int, Lock]

    def __init__(self):
        self.__pool = ThreadPoolExecutor()
        self.__locks = {}

    def solve(self, client: Client, callback: Callable[[Future], Any]):
        self.__pool.submit(self.__run, client).add_done_callback(callback)

    def __run(self, client: Client):
        lock = self.__get_lock(client.client_id)
        with lock:
            return client.algorithm.solve(
                data=client.algorithm_data,
                params=client.algorithm_params,
            )

    def __get_lock(self, client_hash: int):
        if client_hash not in self.__locks:
            self.__locks[client_hash] = Lock()
        return self.__locks[client_hash]


class DataProcess:
    client_manager: ClientManager = ClientManager()
    algorithm_result_queue: AsyncQueue = AsyncQueue()

    __algorithm_solver: AlgorithmSolver = AlgorithmSolver()
    __message_manager: MessageManager = MessageManager()

    __current_client: int | None = None
    __conn: AsyncConnection
    __algorithm_changing: bool = False

    @staticmethod
    def __setup_message_manager():
        DataProcess.__message_manager.set_client_manager(DataProcess.client_manager)

    @staticmethod
    def __setup_client_manager():
        from .process_func import UIFunc

        def add_date_recv_msg(client: Client):
            time_stamp = datetime.now().strftime("%H:%M:%S %f")
            DataProcess.__message_manager.add_message(
                client.client_id, f"Data received at {time_stamp}."
            )

        def update_figures_and_label(client: Client):
            figures = client.algorithm_result.figure_map
            if not client.above_figure_name or client.above_figure_name not in figures:
                name = list(figures.keys())[0]
                DataProcess.client_manager.set_client_data(
                    client.client_id, {"above_figure_name": name}
                )
                client.above_figure_name = name
            if not client.below_figure_name or client.below_figure_name not in figures:
                name = list(figures.keys())[0]
                DataProcess.client_manager.set_client_data(
                    client.client_id, {"below_figure_name": name}
                )
                client.below_figure_name = name
            DataProcess.send_data(
                FuncData(
                    UIFunc.set_figure_combo_box,
                    (figures, client.above_figure_name, client.below_figure_name),
                )
            )
            DataProcess.send_data(
                FuncData(UIFunc.set_result_label, (client.algorithm_result.text,))
            )

        def update_algorithm(client: Client):
            DataProcess.__algorithm_changing = True
            name = client.algorithm_name
            factory = client.algorithm_factory
            algorithm = factory.get_algorithm(name)
            params = algorithm.get_default_params()
            DataProcess.client_manager.set_client_data(
                client.client_id, {"algorithm_params": params}
            )
            DataProcess.__algorithm_changing = False
            DataProcess.client_manager.set_client_data(
                client.client_id, {"algorithm": algorithm}
            )
            DataProcess.send_data(FuncData(UIFunc.set_params, (params,)))

        data_observer = ConditionalObserver(
            lambda _, k: k == "algorithm_data",
            lambda c, _: add_date_recv_msg(c),
        )
        solve_observer = ConditionalObserver(
            lambda _, k: k == "algorithm"
            or k == "algorithm_data"
            or k == "algorithm_params",
            lambda c, _: DataProcess.solve_algorithm(c),
        )
        msg_observer = ConditionalObserver(
            lambda c, k: k == "msg" and c.client_id == DataProcess.__current_client,
            lambda c, _: DataProcess.send_data(FuncData(UIFunc.set_msg, (c.msg,))),
        )
        algorithm_observer = ConditionalObserver(
            lambda _, k: k == "algorithm_name",
            lambda c, _: update_algorithm(c),
        )
        result_observer = ConditionalObserver(
            lambda c, k: k == "algorithm_result"
            and DataProcess.__current_client == c.client_id,
            lambda c, _: update_figures_and_label(c),
        )

        DataProcess.client_manager.set_default_observers(
            [
                data_observer,
                solve_observer,
                msg_observer,
                algorithm_observer,
                result_observer,
            ]
        )

        def add_callback(client: Client):
            id = client.client_id
            name = client.client_name

            DataProcess.send_data(FuncData(UIFunc.add_client, (id, name)))
            DataProcess.__message_manager.add_message(id, f"Client {name} connected.")

        def remove_callback(client_id: int):

            DataProcess.send_data(FuncData(UIFunc.remove_client, (client_id,)))

        DataProcess.client_manager.set_add_client_hook(add_callback)
        DataProcess.client_manager.set_remove_client_hook(remove_callback)

    @staticmethod
    def solve_algorithm(client: Client):
        if DataProcess.__algorithm_changing:
            return
        if (
            client.stop_calculation
            or DataProcess.__current_client != client.client_id
            and not client.backend_calculation
        ):
            if not client.need_update:
                DataProcess.client_manager.set_client_data(
                    client.client_id, {"need_update": True}
                )
            return

        if client.need_update:
            DataProcess.client_manager.set_client_data(
                client.client_id, {"need_update": False}
            )

        DataProcess.__algorithm_solver.solve(
            client,
            lambda f: DataProcess.algorithm_result_queue.put(
                {"client_id": client.client_id, "result": f.result()}
            ),
        )

    @staticmethod
    async def __websocket_run(path: str, port: int):
        callback = BearingWebSocketCallback(DataProcess.client_manager)
        server = WebSocketServer(path, port, callback)
        await server.run()

    @staticmethod
    async def __recv_data(callback: Callable):
        while True:
            callback(await DataProcess.__conn.recv())

    @staticmethod
    async def __recv_algorithm_result():
        def complete_task(client: Client, result: AlgorithmResult):
            try:
                DataProcess.client_manager.set_client_data(
                    client.client_id,
                    {"algorithm_result": result},
                )
                DataProcess.__message_manager.add_message(
                    client.client_id,
                    f"{client.algorithm_name} calculated.",
                )
            except ClientExistError:
                # ignore exist error because client
                # may be removed before calculation completed
                pass

        while True:
            r = await DataProcess.algorithm_result_queue.get()
            client = DataProcess.client_manager.get_client(r["client_id"])
            complete_task(client, r["result"])

    @staticmethod
    def __run_func(func: FuncData):
        func(DataProcess, *func.args, **func.kwargs)

    @staticmethod
    def send_data(data):
        DataProcess.__conn.send(data)

    @staticmethod
    def set_pipe(conn: AsyncConnection):
        DataProcess.__conn = conn

    @staticmethod
    def set_current_client(client_id: int | None):
        DataProcess.__current_client = client_id

    @staticmethod
    def get_current_client() -> int | None:
        return DataProcess.__current_client

    @staticmethod
    def run(path: str, port: int):
        DataProcess.__setup_message_manager()
        DataProcess.__setup_client_manager()

        loop = asyncio.get_event_loop()
        loop.create_task(DataProcess.__recv_data(DataProcess.__run_func))
        loop.create_task(DataProcess.__recv_algorithm_result())
        loop.run_until_complete(DataProcess.__websocket_run(path, port))
