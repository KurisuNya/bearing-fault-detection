import datetime
from enum import Enum
from types import FunctionType

from .client import Client
from .utils.observer import Observer


class MessageLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MessageManager:
    max_lines = 20

    @staticmethod
    def add_message(level: MessageLevel, old_msg: str, new_msg: str) -> str:
        new_msg = f"[{level.name}] {new_msg}"
        if old_msg == "":
            return new_msg
        split_msg = old_msg.split("\n")
        if len(split_msg) >= MessageManager.max_lines:
            split_msg = split_msg[1:]
        return "\n".join(split_msg) + "\n" + new_msg


class ClientManager:
    __client_map: dict[int, Client]
    __default_observers: Observer | list[Observer]

    __add_client_hook: FunctionType
    __remove_client_hook: FunctionType

    def __init__(
        self,
        default_observers: Observer | list[Observer] = [],
        add_client_hook: FunctionType = lambda client_id, client: None,  # type: ignore
        remove_client_hook: FunctionType = lambda client_id: None,  # type: ignore
    ):
        self.__client_map = {}
        self.__default_observers = default_observers
        self.__add_client_hook = add_client_hook
        self.__remove_client_hook = remove_client_hook

    def add_client(self, client: Client):
        client_id = client.client_id
        self.__check_client_not_exist(client_id)
        client.attach(self.__default_observers)
        self.__client_map[client_id] = client
        self.__add_client_hook(client_id, client)

    def remove_client(self, client_id: int):
        self.__check_client_exist(client_id)
        del self.__client_map[client_id]
        self.__remove_client_hook(client_id)

    def set_client_data(self, client_id: int, data: dict):
        self.__check_client_exist(client_id)
        for key, value in data.items():
            self.__client_map[client_id][key] = value

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

    def set_default_observers(self, observers: Observer | list[Observer]):
        self.__default_observers = observers

    def add_default_observers(self, observers: Observer | list[Observer]):
        def to_list(obj):
            if not isinstance(obj, list):
                return [obj]
            return obj

        if not isinstance(self.__default_observers, list):
            self.__default_observers = [self.__default_observers, *to_list(observers)]
        else:
            self.__default_observers = [*self.__default_observers, *to_list(observers)]

    def __check_client_exist(self, client_id: int):
        if not self.is_client_exists(client_id):
            raise ValueError("Client does not exist")

    def __check_client_not_exist(self, client_id: int):
        if self.is_client_exists(client_id):
            raise ValueError("Client already exists")

    def __add_connection_message(self, client_id: int):
        name = self.__client_map[client_id].client_name
        self.add_message(client_id, f"Client {name} connected.")
        self.add_message(
            client_id, f"Config: {self.__client_map[client_id].algorithm_data.cfg}."
        )

    def __add_data_recv_msg(self, client_id: int):
        time_stamp = datetime.datetime.now().strftime("%H:%M:%S %f")
        self.add_message(client_id, "Data received at " + time_stamp + ".")
