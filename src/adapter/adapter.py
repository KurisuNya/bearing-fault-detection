from abc import ABCMeta, abstractmethod

from .algorithm import ClientData
from .algorithm.interface import AlgorithmFactory
from .algorithm.test_device import TestDeviceAlgorithmFactory
from .algorithm.icm20948 import ICM20948AlgorithmFactory


class Adapter(metaclass=ABCMeta):
    @abstractmethod
    def get_client_data(self, msg: dict) -> ClientData:
        pass

    @abstractmethod
    def get_algorithm_factory(self) -> AlgorithmFactory:
        pass


class TestAdapter(Adapter):
    def get_client_data(self, msg: dict) -> ClientData:
        return ClientData(cfg=msg["cfg"], data=msg["data"])

    def get_algorithm_factory(self) -> AlgorithmFactory:
        return TestDeviceAlgorithmFactory()


class ICM20948Adapter(Adapter):
    def get_client_data(self, msg: dict) -> ClientData:
        cfg = {
            "acc_range": msg["acc_range"],
            "acc_sample_rate": msg["acc_sample_rate"],
            "acc_sample_dots": msg["acc_sample_dots"],
        }
        hex_str = msg["data"]
        data = bytearray.fromhex(hex_str)
        data = [
            int.from_bytes(data[i : i + 4], "little") for i in range(0, len(data), 4)
        ]
        return ClientData(cfg=cfg, data={"data": data})

    def get_algorithm_factory(self) -> AlgorithmFactory:
        return ICM20948AlgorithmFactory()


class AdapterFactory:
    @staticmethod
    def get_adapter(device_type: str) -> Adapter:
        if device_type == "Test":
            return TestAdapter()
        if device_type == "ICM20948":
            return ICM20948Adapter()
        else:
            raise ValueError("Unknown device type")
