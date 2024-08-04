from abc import ABCMeta, abstractmethod
from typing import Any

from .utils import ParamError


class ParamType(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def to_string(value: Any) -> str:
        pass

    @staticmethod
    @abstractmethod
    def to_value(string: str) -> Any:
        pass


class IntType(ParamType):
    @staticmethod
    def to_string(value: Any) -> str:
        return str(value)

    @staticmethod
    def to_value(string: str) -> Any:
        try:
            return int(string)
        except ValueError:
            raise ParamError("Invalid int value")


class FloatType(ParamType):
    @staticmethod
    def to_string(value: Any) -> str:
        return str(value)

    @staticmethod
    def to_value(string: str) -> Any:
        try:
            return float(string)
        except ValueError:
            raise ParamError("Invalid float value")


class StrType(ParamType):
    @staticmethod
    def to_string(value: Any) -> str:
        return str(value)

    @staticmethod
    def to_value(string: str) -> Any:
        return string
