from copy import deepcopy
from typing import Any, Callable

from .client import Client
from .utils.observer import Observer


class ClientExistError(Exception):
    pass


class ClientManager:
    __client_map: dict[int, Client]
    __default_observers: Observer | list[Observer]

    __add_client_hook: Callable[[Client], Any]
    __remove_client_hook: Callable[[int], Any]

    def __init__(
        self,
        default_observers: Observer | list[Observer] = [],
        add_client_hook: Callable[[Client], Any] = lambda client: None,
        remove_client_hook: Callable[[int], Any] = lambda client_id: None,
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
        self.__add_client_hook(client)

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
        return deepcopy(self.__client_map[client_id][key])

    def get_client(self, client_id: int) -> Client:
        self.__check_client_exist(client_id)
        client = deepcopy(self.__client_map[client_id])
        client.detach_all()
        return client

    def is_client_exists(self, client_id: int) -> bool:
        return client_id in self.__client_map

    def set_default_observers(self, observers: Observer | list[Observer]):
        self.__default_observers = observers

    def set_add_client_hook(self, hook: Callable[[Client], Any]):
        self.__add_client_hook = hook

    def set_remove_client_hook(self, hook: Callable[[int], Any]):
        self.__remove_client_hook = hook

    def __check_client_exist(self, client_id: int):
        if not self.is_client_exists(client_id):
            raise ClientExistError("Client does not exist")

    def __check_client_not_exist(self, client_id: int):
        if self.is_client_exists(client_id):
            raise ClientExistError("Client already exists")
