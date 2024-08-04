from enum import Enum
from .client_manager import ClientManager


class MessageLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MessageManager:
    __client_manager: ClientManager | None
    __max_lines: int

    def __init__(
        self, client_manager: ClientManager | None = None, max_lines: int = 500
    ):
        self.__client_manager = client_manager
        self.__max_lines = max_lines

    def set_client_manager(self, client_manager: ClientManager):
        self.__client_manager = client_manager

    def add_message(
        self, client_id: int, msg: str, level: MessageLevel = MessageLevel.INFO
    ):
        if self.__client_manager is None:
            raise ValueError("Client manager is not set")

        old_msg = self.__client_manager.get_client_data(client_id, "msg")
        new_msg = self.__generate_msg(level, old_msg, msg)
        self.__client_manager.set_client_data(client_id, {"msg": new_msg})

    def __generate_msg(self, level: MessageLevel, old_msg: str, new_msg: str) -> str:
        new_msg = f"[{level.name}] {new_msg}"
        if old_msg == "":
            return new_msg
        split_msg = old_msg.split("\n")
        if len(split_msg) >= self.__max_lines:
            split_msg = split_msg[1:]
        return "\n".join(split_msg) + "\n" + new_msg
