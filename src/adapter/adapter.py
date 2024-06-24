from abc import ABCMeta, abstractmethod

from .algorithm import AlgorithmData
from .algorithm.device.icm20948 import ICM20948AlgorithmFactory
from .algorithm.device.test_device import TestDeviceAlgorithmFactory
from .algorithm.interface import AlgorithmFactory


class Adapter(metaclass=ABCMeta):
    @abstractmethod
    def get_algorithm_data(self, msg: dict) -> AlgorithmData:
        pass

    @abstractmethod
    def get_algorithm_factory(self) -> AlgorithmFactory:
        pass


class TestAdapter(Adapter):
    def get_algorithm_data(self, msg: dict) -> AlgorithmData:
        return AlgorithmData(cfg=msg["cfg"], data=msg["data"])

    def get_algorithm_factory(self) -> AlgorithmFactory:
        return TestDeviceAlgorithmFactory()


class ICM20948Adapter(Adapter):
    def get_algorithm_data(self, msg: dict) -> AlgorithmData:
        cfg = {
            "accelerate_range": msg["acc_range"],
            "sample_rate": msg["acc_sample_rate"],
            "sample_dots": msg["acc_sample_dots"],
        }
        data = {"data": self.__convert_from_hex(msg["data"])}
        return AlgorithmData(cfg=cfg, data=data)

    def get_algorithm_factory(self) -> AlgorithmFactory:
        return ICM20948AlgorithmFactory()

    def __convert_from_hex(self, hex_str: str) -> list[int]:
        byte_array = bytearray.fromhex(hex_str)
        return [
            int.from_bytes(byte_array[i : i + 4], "little")
            for i in range(0, len(byte_array), 4)
        ]


class AdapterFactory:
    @staticmethod
    def get_adapter(device_type: str) -> Adapter:
        if device_type == "Test":
            return TestAdapter()
        if device_type == "ICM20948":
            return ICM20948Adapter()
        else:
            raise ValueError("Unknown device type")
