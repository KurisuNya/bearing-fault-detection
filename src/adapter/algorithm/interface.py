from abc import ABCMeta, abstractmethod

from .client_data import ClientData
from .param import Param


class Algorithm(metaclass=ABCMeta):
    @abstractmethod
    def solve(self, data: ClientData, params: dict[str, Param]):
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
