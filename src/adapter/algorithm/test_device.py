from dataclasses import asdict

from .client_data import ClientData
from .interface import Algorithm, AlgorithmError, AlgorithmFactory
from .param import Param, ParamError


class TestAlgorithm(Algorithm):
    def solve(self, data: ClientData, params: dict[str, Param]):
        self.__check_params(params)
        print("Algorithm received data: ", asdict(data))
        print(
            "Algorithm received params: ", {k: v.get_value() for k, v in params.items()}
        )

    def __check_params(self, params: dict[str, Param]):
        for key, param in params.items():
            if not param.get_value():
                raise AlgorithmError(f"Parameter {key} is not set")

    def get_default_params(self) -> dict[str, Param]:
        def check_type(value):
            if not isinstance(value, int):
                raise ParamError("Value must be an integer")

        def check_range(value):
            if value < 0 or value > 100:
                raise ParamError("Value must be between 0 and 100")

        def check_step(value):
            if value % 10 != 0:
                raise ParamError("Value must be a multiple of 10")

        return {
            "param1": Param(
                value=10,
                check_funcs=[check_type, check_range],
            ),
            "param2": Param(
                value=20,
                check_funcs=[check_type, check_range, check_step],
            ),
        }


class TestDeviceAlgorithmFactory(AlgorithmFactory):
    @staticmethod
    def get_algorithm(algorithm_name: str) -> Algorithm:
        if algorithm_name == "Test":
            return TestAlgorithm()
        else:
            raise ValueError("Unknown algorithm name")

    @staticmethod
    def get_algorithm_names() -> list[str]:
        return ["Test"]
