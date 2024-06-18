from enum import Enum


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
