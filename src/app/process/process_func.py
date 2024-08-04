from typing import Any, Callable

from matplotlib.figure import Figure

from ..utils import FuncData
from .data_process import DataProcess
from .ui_process import UIProcess


class UIFunc:

    @staticmethod
    def add_client(process: UIProcess, client_id: int, client_name: str):
        process.window.add_client(client_id, client_name)

    @staticmethod
    def remove_client(process: UIProcess, client_id: int):
        process.window.remove_client(client_id)

    @staticmethod
    def set_msg(process: UIProcess, msg: str):
        process.window.set_msg(msg)

    @staticmethod
    def set_stop_calculation_state(process: UIProcess, state: bool):
        process.window.set_stop_calculation_state(state)

    @staticmethod
    def set_backend_calculation_state(process: UIProcess, state: bool):
        process.window.set_backend_calculation_state(state)

    @staticmethod
    def set_figure_combo_box(
        process: UIProcess,
        figures: dict[str, Figure],
        above_name: str,
        below_name: str,
    ):
        process.window.set_figure_combo_box(figures, above_name, below_name)

    @staticmethod
    def set_result_label(process: UIProcess, result: str):
        process.window.set_result_label(result)

    @staticmethod
    def set_algorithm_combo_box(process: UIProcess, names: list[str], name: str):
        process.window.set_algorithm_combo_box(names, name)

    @staticmethod
    def set_params(process: UIProcess, params: dict[str, Any]):
        process.window.set_params(params)


class DataFunc:

    @staticmethod
    def set_current_client(process: DataProcess, client_id: int):
        process.set_current_client(client_id)

    @staticmethod
    def get_client_data(
        process: DataProcess,
        client_id: int,
        key: str,
        callback: Callable,
    ):
        data = process.client_manager.get_client_data(client_id, key)
        process.send_data(FuncData(callback, (data,)))

    @staticmethod
    def set_client_data(process: DataProcess, client_id: int, data: dict[str, Any]):
        process.client_manager.set_client_data(client_id, data)

    @staticmethod
    def set_current_client_data(process: DataProcess, data: dict[str, Any]):
        client_id = process.get_current_client()
        if not client_id:
            return
        process.client_manager.set_client_data(client_id, data)

    @staticmethod
    def solve_algorithm(process: DataProcess, client_id: int):
        client = process.client_manager.get_client(client_id)
        if client.need_update:
            process.solve_algorithm(client)

    @staticmethod
    def solve_current_client_algorithm(process: DataProcess):
        client_id = process.get_current_client()
        if not client_id:
            return
        DataFunc.solve_algorithm(process, client_id)

    @staticmethod
    def get_figure_combo_box(process: DataProcess, client_id: int, callback: Callable):
        client = process.client_manager.get_client(client_id)
        if len(client.algorithm_result.figure_map) == 0:
            return
        figures = client.algorithm_result.figure_map
        if not client.above_figure_name:
            name = list(figures.keys())[0]
            process.client_manager.set_client_data(
                client.client_id, {"above_figure_name": name}
            )
            client.above_figure_name = name
        if not client.below_figure_name:
            name = list(figures.keys())[0]
            process.client_manager.set_client_data(
                client.client_id, {"below_figure_name": name}
            )
            client.below_figure_name = name
        process.send_data(
            FuncData(
                callback,
                (
                    figures,
                    client.above_figure_name,
                    client.below_figure_name,
                ),
            )
        )

    @staticmethod
    def get_result_text(process: DataProcess, client_id: int, callback: Callable):
        client = process.client_manager.get_client(client_id)
        result = client.algorithm_result.text
        process.send_data(FuncData(callback, (result,)))

    @staticmethod
    def get_algorithm_combo_box(
        process: DataProcess, client_id: int, callback: Callable
    ):
        client = process.client_manager.get_client(client_id)
        name = client.algorithm_name
        factory = client.algorithm_factory
        process.send_data(FuncData(callback, (factory.get_algorithm_names(), name)))
