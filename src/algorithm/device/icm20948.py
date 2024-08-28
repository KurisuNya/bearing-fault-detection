from dataclasses import asdict

from ..algorithm_data import AlgorithmData, AlgorithmResult
from ..interface import Algorithm, AlgorithmError, AlgorithmFactory
from ..param import (
    FloatType,
    IntType,
    NotSpecificChecker,
    Param,
    RangeChecker,
    SpecificChecker,
    StepChecker,
    StrType,
)


class ICM20948TestAlgorithm(Algorithm):
    def solve(self, data: AlgorithmData, params: dict[str, Param]) -> AlgorithmResult:
        print("Algorithm received data: ", asdict(data))
        print(
            "Algorithm received params: ", {k: v.get_value() for k, v in params.items()}
        )
        return AlgorithmResult({}, "Test algorithm result")

    def get_default_params(self) -> dict[str, Param]:
        range_checker = RangeChecker(
            min=0,
            max=100,
            left_open=False,
            right_open=False,
        )
        step_checker = StepChecker(step=10)

        return {
            "param1": Param(
                type=IntType(),
                value=10,
                checkers=[range_checker],
            ),
            "param2": Param(
                type=IntType(),
                value=20,
                checkers=[range_checker, step_checker],
            ),
        }


class ICM20948AlgorithmFactory(AlgorithmFactory):
    @staticmethod
    def get_algorithm(algorithm_name: str) -> Algorithm:
        if algorithm_name == "Test":
            return ICM20948TestAlgorithm()
        else:
            raise ValueError("Unknown algorithm name")

    @staticmethod
    def get_algorithm_names() -> list[str]:
        return ["Test"]
