from multiprocessing import Process

from .process import DataProcess, UIProcess
from .utils import AsyncPipe


class App:
    __data_process: Process
    __ui_process: Process

    @staticmethod
    def __setup_processes(path: str, port: int):
        p1, p2 = AsyncPipe()
        DataProcess.set_pipe(p1)
        UIProcess.set_pipe(p2)
        App.__data_process = Process(target=DataProcess.run, args=(path, port))
        App.__ui_process = Process(target=UIProcess.run)

    @staticmethod
    def __run_processes():
        App.__ui_process.start()
        App.__data_process.start()

    @staticmethod
    def __run_until_ui_closed():
        App.__ui_process.join()
        App.__data_process.terminate()

    @staticmethod
    def run(path: str, port: int):
        App.__setup_processes(path, port)
        App.__run_processes()
        App.__run_until_ui_closed()
