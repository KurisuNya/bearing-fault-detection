import os
import sys
from typing import Callable

import PySide6.QtAsyncio as QtAsyncio
from PySide6.QtWidgets import QApplication

from ...algorithm.param import Param
from ...gui.window import MainWindow
from ..utils import AsyncConnection, FuncData


class UIProcess:
    window: MainWindow

    __conn: AsyncConnection

    @staticmethod
    async def __recv_data(callback: Callable):
        while True:
            callback(await UIProcess.__conn.recv())

    @staticmethod
    def __run_func(func: FuncData):
        func(UIProcess, *func.args, **func.kwargs)

    @staticmethod
    def __setup_window():
        from .process_func import DataFunc, UIFunc

        def client_change_hook(client_id: int | None):
            update_current_client(client_id)
            update_msg(client_id)
            update_algorithm_combo_box(client_id)
            update_figures_and_label(client_id)
            update_params(client_id)
            update_stop_calculation_button(client_id)
            update_backend_checkbox(client_id)
            update_algorithm_result(client_id)

        def update_current_client(client_id: int | None):
            UIProcess.send_data(FuncData(DataFunc.set_current_client, (client_id,)))

        def update_algorithm_combo_box(client_id: int | None):
            if not client_id:
                UIProcess.window.clear_algorithm_combobox()
                return
            UIProcess.send_data(
                FuncData(
                    DataFunc.get_algorithm_combo_box,
                    (client_id, UIFunc.set_algorithm_combo_box),
                )
            )

        def update_stop_calculation_button(client_id: int | None):
            if not client_id:
                UIProcess.window.set_stop_calculation_button(False)
                return
            UIProcess.window.set_stop_calculation_button(True)
            func = FuncData(
                DataFunc.get_client_data,
                (
                    client_id,
                    "stop_calculation",
                    UIFunc.set_stop_calculation_state,
                ),
            )
            UIProcess.send_data(func)

        def update_backend_checkbox(client_id: int | None):
            if not client_id:
                UIProcess.window.set_backend_calculation_checkbox(False)
                return
            UIProcess.window.set_backend_calculation_checkbox(True)
            func = FuncData(
                DataFunc.get_client_data,
                (
                    client_id,
                    "backend_calculation",
                    UIFunc.set_backend_calculation_state,
                ),
            )
            UIProcess.send_data(func)

        def update_msg(client_id: int | None):
            if not client_id:
                UIProcess.window.set_msg("")
                return
            UIProcess.send_data(
                FuncData(DataFunc.get_client_data, (client_id, "msg", UIFunc.set_msg))
            )

        def update_params(client_id: int | None):
            if not client_id:
                UIProcess.window.clear_params()
                return
            UIProcess.send_data(
                FuncData(
                    DataFunc.get_client_data,
                    (client_id, "algorithm_params", UIFunc.set_params),
                )
            )

        def update_figures_and_label(client_id: int | None):
            if not client_id:
                UIProcess.window.clear_figure_combo_box()
                UIProcess.window.set_result_label("")
                return
            UIProcess.send_data(
                FuncData(
                    DataFunc.get_figure_combo_box,
                    (client_id, UIFunc.set_figure_combo_box),
                )
            )
            UIProcess.send_data(
                FuncData(
                    DataFunc.get_result_text,
                    (client_id, UIFunc.set_result_label),
                )
            )

        def update_algorithm_result(client_id: int | None):
            if not client_id:
                return
            UIProcess.send_data(FuncData(DataFunc.solve_algorithm, (client_id,)))

        def stop_calculation_hook(state: bool):
            if not state:
                UIProcess.send_data(FuncData(DataFunc.solve_current_client_algorithm))
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"stop_calculation": state},),
                )
            )

        def backend_calculation_hook(state: bool):
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"backend_calculation": state},),
                )
            )

        def above_figure_change_hook(name: str):
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"above_figure_name": name},),
                )
            )

        def below_figure_change_hook(name: str):
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"below_figure_name": name},),
                )
            )

        def algorithm_change_hook(name: str):
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"algorithm_name": name},),
                )
            )

        def params_change_hook(params: dict[str, Param]):
            UIProcess.send_data(
                FuncData(
                    DataFunc.set_current_client_data,
                    ({"algorithm_params": params},),
                )
            )

        UIProcess.window.set_client_change_hook(client_change_hook)
        UIProcess.window.set_algorithm_change_hook(algorithm_change_hook)
        UIProcess.window.set_stop_calculation_hook(stop_calculation_hook)
        UIProcess.window.set_backend_calculation_hook(backend_calculation_hook)
        UIProcess.window.set_above_figure_change_hook(above_figure_change_hook)
        UIProcess.window.set_below_figure_change_hook(below_figure_change_hook)
        UIProcess.window.set_params_change_hook(params_change_hook)

    @staticmethod
    def __quit_all():
        os._exit(0)

    @staticmethod
    def send_data(data):
        UIProcess.__conn.send(data)

    @staticmethod
    def set_pipe(conn: AsyncConnection):
        UIProcess.__conn = conn

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        app.aboutToQuit.connect(UIProcess.__quit_all)
        UIProcess.window = MainWindow(magnet_distance=1)
        UIProcess.__setup_window()
        UIProcess.window.show()
        QtAsyncio.run(UIProcess.__recv_data(UIProcess.__run_func))
