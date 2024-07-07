from abc import ABCMeta, abstractmethod

from .algorithm_data import AlgorithmData, AlgorithmResult
from .param import Param


class Algorithm(metaclass=ABCMeta):
    @abstractmethod
    def solve(self, data: AlgorithmData, params: dict[str, Param]) -> AlgorithmResult:
        pass

    @abstractmethod
    def get_default_params(self) -> dict[str, Param]:
        pass


class AlgorithmError(Exception):
    pass


class AlgorithmFactory(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_algorithm(algorithm_name: str) -> Algorithm:
        pass

    @staticmethod
    @abstractmethod
    def get_algorithm_names() -> list[str]:
        pass
