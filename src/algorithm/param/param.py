from typing import Any
from .param_type import ParamType
from .param_checker import ParamChecker


class Param:
    __checkers: list
    __value: Any = None
    __type: ParamType

    def __init__(
        self,
        type: ParamType,
        value: Any = None,
        checkers: list[ParamChecker] = [],
    ):
        self.__checkers = checkers
        self.__type = type
        if value:
            self.set_value(value)

    def add_check_func(self, check_func):
        self.__checkers.append(check_func)

    def get_value(self) -> Any:
        return self.__value

    def set_value(self, value: Any):
        for checker in self.__checkers:
            checker.check(value)
        self.__value = value

    def get_type(self) -> ParamType:
        return self.__type

    def set_type(self, type: ParamType):
        self.__type = type
