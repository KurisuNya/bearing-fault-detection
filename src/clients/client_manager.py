import datetime
from types import FunctionType

from .client import Client
from .utils.message_manager import MessageLevel, MessageManager
from .utils.observer import Observer


class ClientManager:
    __client_map: dict[int, Client]
    __default_observers: Observer | list[Observer]

    __add_client_hook: FunctionType
    __remove_client_hook: FunctionType

    def __init__(
        self,
        client_observers: Observer | list[Observer],
        add_client_hook: FunctionType = lambda client_id, client: None,  # type: ignore
        remove_client_hook: FunctionType = lambda client_id: None,  # type: ignore
    ):
        self.__client_map = {}
        self.__default_observers = client_observers
        self.__add_client_hook = add_client_hook
        self.__remove_client_hook = remove_client_hook

    def add_client(
        self,
        client_id: int,
        client: Client,
    ):
        self.__check_client_not_exist(client_id)
        client.attach(self.__default_observers)
        self.__client_map[client_id] = client
        self.__add_connection_message(client_id)
        self.__add_client_hook(client_id, client)

    def remove_client(self, client_id: int):
        self.__check_client_exist(client_id)
        del self.__client_map[client_id]
        self.__remove_client_hook(client_id)

    def set_client_data(self, client_id: int, data: dict):
        self.__check_client_exist(client_id)
        for key, value in data.items():
            self.__client_map[client_id][key] = value
        self.__add_data_recv_msg(client_id)

    def get_client_data(self, client_id: int, key: str):
        self.__check_client_exist(client_id)
        return self.__client_map[client_id][key]

    def is_client_exists(self, client_id: int) -> bool:
        return client_id in self.__client_map

    def add_message(
        self, client_id: int, msg: str, level: MessageLevel = MessageLevel.INFO
    ):
        self.__client_map[client_id].msg = MessageManager.add_message(
            level, self.__client_map[client_id].msg, msg
        )

    def attach_observers(self, client_id: int, observers: Observer | list[Observer]):
        self.__check_client_exist(client_id)
        self.__client_map[client_id].attach(observers)

    def detach_observers(self, client_id: int, observers: Observer | list[Observer]):
        self.__check_client_exist(client_id)
        self.__client_map[client_id].detach(observers)

    def __add_connection_message(self, client_id: int):
        name = self.__client_map[client_id].client_name
        self.add_message(client_id, f"Client {name} connected.")
        self.add_message(
            client_id, f"Config: {self.__client_map[client_id].algorithm_data.cfg}."
        )
        self.__add_data_recv_msg(client_id)

    def __add_data_recv_msg(self, client_id: int):
        time_stamp = datetime.datetime.now().strftime("%H:%M:%S %f")
        self.add_message(client_id, "Data received at " + time_stamp + ".")

    def __check_client_exist(self, client_id: int):
        if not self.is_client_exists(client_id):
            raise ValueError("Client does not exist")

    def __check_client_not_exist(self, client_id: int):
        if self.is_client_exists(client_id):
            raise ValueError("Client already exists")
