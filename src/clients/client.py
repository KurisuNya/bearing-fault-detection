from copy import deepcopy
from dataclasses import asdict, dataclass, field

from ..adapter.algorithm import ClientData
from ..adapter.algorithm.interface import Algorithm, AlgorithmFactory
from ..adapter.algorithm.param import Param
from .utils.observer import Observable


@dataclass
class Client(Observable):
    client_hash: int
    client_name: str
    algorithm_factory: AlgorithmFactory

    algorithm: Algorithm
    algorithm_params: dict[str, Param]
    client_data: ClientData = field(default_factory=lambda: ClientData({}, {}))
    figure_list: list = field(default_factory=list)
    label_text: str = ""

    algorithm_index: int = 0
    above_figure_index: int = 0
    below_figure_index: int = 0
    backend_calculation: bool = False

    msg: str = ""

    __observers = []

    @staticmethod
    def __to_list(obj):
        if not isinstance(obj, list):
            return [obj]
        return obj

    def attach(self, observers):
        self.__observers = [
            *self.__observers,
            *self.__to_list(observers),
        ]

    def detach(self, observers):
        for obs in self.__to_list(observers):
            self.__observers.remove(obs)

    def detach_all(self):
        self.__observers = []

    def notify(self, keys):
        for observer in self.__observers:
            for keys in self.__to_list(keys):
                observer.update(deepcopy(self), keys)

    def notify_all(self):
        for observer in self.__observers:
            for key in list(asdict(self).keys()):
                observer.update(deepcopy(self), key)

    def __setattr__(self, key, value):
        if not hasattr(self, key) or "__observers" in key:
            super().__setattr__(key, value)
            return
        if getattr(self, key) != value:
            super().__setattr__(key, value)
            self.notify(key)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
