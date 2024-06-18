import asyncio
from datetime import time
import json

import websockets


async def echo(path, port):
    async with websockets.connect(f"ws://{path}:{port}") as websocket:
        device_type = "Test"
        cfg = {"a": 1, "b": 2}
        data = 0
        while True:
            data += 1
            await asyncio.sleep(1)
            await websocket.send(
                json.dumps({"device_type": device_type, "cfg": cfg, "data": data})
            )


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(echo("localhost", 8765))
