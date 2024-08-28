import asyncio
import json
import websockets


async def loop_send(path, port):
    async with websockets.connect(f"ws://{path}:{port}") as websocket:
        device_type = "Test"
        cfg = {"a": 1, "b": 2}
        data = 0
        while True:
            data += 1
            await websocket.send(
                json.dumps({"device_type": device_type, "cfg": cfg, "data": data})
            )
            await asyncio.sleep(1)


def run(host: str, port: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_send(host, port))


if __name__ == "__main__":
    run("localhost", 2333)
