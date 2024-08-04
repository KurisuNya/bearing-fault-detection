import asyncio
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pipe, Queue
from multiprocessing.connection import Connection
from typing import Any


class AsyncConnection:
    def __init__(self, conn: Connection):
        self.__conn = conn

    def send(self, value: Any):
        self.__conn.send(value)

    async def recv(self):
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.__conn.recv)


def AsyncPipe():
    c1, c2 = Pipe()
    return AsyncConnection(c1), AsyncConnection(c2)


class AsyncQueue:
    def __init__(self):
        self.__queue = Queue()

    def put(self, value: Any):
        self.__queue.put(value)

    async def get(self):
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.__queue.get)

    def empty(self):
        return self.__queue.empty()

    def qsize(self):
        return self.__queue.qsize()
