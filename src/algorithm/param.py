from typing import Any


class ParamError(Exception):
    pass


class Param:
    __check_funcs: list
    __value: Any = None
    __type: type

    def __init__(self, type: type, value: Any = None, check_funcs: list = []):
        self.__check_funcs = check_funcs
        self.__type = type
        if value:
            self.set_value(value)

    def add_check_func(self, check_func):
        self.__check_funcs.append(check_func)

    def get_value(self) -> Any:
        return self.__value

    def set_value(self, value: Any):
        for check_func in self.__check_funcs:
            check_func(value)
        self.__value = value

    def get_type(self) -> type:
        return self.__type

    def set_type(self, type: type):
        self.__type = type
