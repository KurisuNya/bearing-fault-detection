from abc import ABCMeta, abstractmethod
from typing import Any

from .utils import ParamError


class ParamChecker(metaclass=ABCMeta):

    @abstractmethod
    def check(self, value: Any):
        pass


class RangeChecker(ParamChecker):
    def __init__(
        self, min: Any, max: Any, left_open: bool = False, right_open: bool = False
    ):
        self.__min = min
        self.__max = max
        self.__left_open = left_open
        self.__right_open = right_open

    def check(self, value: Any):
        try:
            min = self.__min
            max = self.__max
            left_open = self.__left_open
            right_open = self.__right_open

            if left_open and value <= min:
                raise ParamError(f"Value must be greater than {min}")
            if not left_open and value < min:
                raise ParamError(f"Value must be greater than or equal to {min}")
            if right_open and value >= max:
                raise ParamError(f"Value must be less than {max}")
            if not right_open and value > max:
                raise ParamError(f"Value must be less than or equal to {max}")

        except ValueError:
            raise ParamError("Invalid range values")


class StepChecker(ParamChecker):

    def __init__(self, step: Any):
        self.__step = step

    def check(self, value: Any):
        try:
            step = self.__step
            if value % step != 0:
                raise ParamError(f"Value must be a multiple of {step}")
        except ValueError:
            raise ParamError("Invalid step value")


class SpecificChecker(ParamChecker):
    def __init__(self, specific: set):
        self.__specific = specific

    def check(self, value: Any):
        try:
            specific = self.__specific
            if value not in specific:
                raise ParamError(f"Value must be one of {specific}")
        except ValueError:
            raise ParamError("Invalid specific value")


class NotSpecificChecker(ParamChecker):
    def __init__(self, specific: set):
        self.__specific = specific

    def check(self, value: Any):
        try:
            specific = self.__specific
            if value in specific:
                raise ParamError(f"Value must not be one of {specific}")
        except ValueError:
            raise ParamError("Invalid specific value")
