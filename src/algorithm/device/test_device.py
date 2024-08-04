from datetime import datetime

from matplotlib.figure import Figure

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


class TestAlgorithm_01(Algorithm):
    def solve(self, data: AlgorithmData, params: dict[str, Param]) -> AlgorithmResult:
        self.__check_params(params)
        figure1 = Figure()
        figure2 = Figure()
        figure1.subplots().text(0, 0.5, f"Figure 1 ({datetime.now()})", fontsize=20)
        figure2.subplots().text(0, 0.5, f"Figure 2 ({datetime.now()})", fontsize=20)

        param1 = params["param1"].get_value()
        param2 = params["param2"].get_value()
        param3 = params["param3"].get_value()

        return AlgorithmResult(
            {
                "figure1": figure1,
                "figure2": figure2,
            },
            f"Test algorithm 01, P1: {param1}, P2: {param2}, P3: {param3}",
        )

    def __check_params(self, params: dict[str, Param]):
        for key, param in params.items():
            if not param.get_value():
                raise AlgorithmError(f"Parameter {key} is not set")

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
                checkers=[
                    range_checker,
                    step_checker,
                ],
            ),
            "param2": Param(
                type=FloatType(),
                value=20,
                checkers=[range_checker],
            ),
            "param3": Param(
                type=StrType(),
                value="test",
                checkers=[
                    SpecificChecker({"test", "test2"}),
                ],
            ),
        }


class TestAlgorithm_02(Algorithm):
    def solve(self, data: AlgorithmData, params: dict[str, Param]) -> AlgorithmResult:
        self.__check_params(params)
        figure1 = Figure()
        figure2 = Figure()
        figure1.subplots().text(0, 0.5, f"Figure 3 ({datetime.now()})", fontsize=20)
        figure2.subplots().text(0, 0.5, f"Figure 4 ({datetime.now()})", fontsize=20)

        param4 = params["param4"].get_value()
        param5 = params["param5"].get_value()
        param6 = params["param6"].get_value()

        return AlgorithmResult(
            {
                "figure3": figure1,
                "figure4": figure2,
            },
            f"Test algorithm 02, P4: {param4}, P5: {param5}, P6: {param6}",
        )

    def __check_params(self, params: dict[str, Param]):
        for key, param in params.items():
            if not param.get_value():
                raise AlgorithmError(f"Parameter {key} is not set")

    def get_default_params(self) -> dict[str, Param]:
        range_checker = RangeChecker(
            min=0,
            max=100,
            left_open=False,
            right_open=False,
        )
        step_checker = StepChecker(step=10)

        return {
            "param4": Param(
                type=IntType(),
                value=10,
                checkers=[range_checker],
            ),
            "param5": Param(
                type=IntType(),
                value=20,
                checkers=[range_checker, step_checker],
            ),
            "param6": Param(
                type=StrType(),
                value="test",
                checkers=[
                    SpecificChecker({"test", "test2"}),
                ],
            ),
        }


class TestDeviceAlgorithmFactory(AlgorithmFactory):
    @staticmethod
    def get_algorithm(algorithm_name: str) -> Algorithm:
        if algorithm_name == "Test01":
            return TestAlgorithm_01()
        if algorithm_name == "Test02":
            return TestAlgorithm_02()
        else:
            raise ValueError("Unknown algorithm name")

    @staticmethod
    def get_algorithm_names() -> list[str]:
        return [
            "Test01",
            "Test02",
        ]
