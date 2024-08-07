from copy import deepcopy
from dataclasses import asdict, dataclass, field

from ..algorithm import AlgorithmData, AlgorithmResult
from ..algorithm.interface import Algorithm, AlgorithmFactory
from ..algorithm.param import Param
from .utils.observer import Observable


@dataclass
class Client(Observable):
    # fixed parameters
    client_id: int
    client_name: str
    algorithm_factory: AlgorithmFactory

    # algorithm parameters
    algorithm: Algorithm
    algorithm_params: dict[str, Param]
    algorithm_data: AlgorithmData = field(default_factory=lambda: AlgorithmData({}, {}))
    algorithm_result: AlgorithmResult = field(
        default_factory=lambda: AlgorithmResult({}, "")
    )

    # gui parameters
    msg: str = ""
    algorithm_name: str = ""
    above_figure_name: str | None = None
    below_figure_name: str | None = None

    # flags
    backend_calculation: bool = False
    stop_calculation: bool = False
    need_update: bool = False

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
            for key in self.__to_list(keys):
                client = deepcopy(self)
                client.detach_all()
                observer.update(client, key)

    def notify_all(self):
        for observer in self.__observers:
            for key in list(asdict(self).keys()):
                client = deepcopy(self)
                client.detach_all()
                observer.update(client, key)

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
