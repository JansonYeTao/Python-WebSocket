import asyncio
import json

import websockets


WS_URL = "ws://localhost:8000/ws"


async def run_client() -> None:
    print(f"Connecting to {WS_URL} ...")
    async with websockets.connect(WS_URL) as websocket:
        hello = await websocket.recv()
        print(f"[server] {hello}")

        print("Type messages and press Enter. Type '/quit' to exit.")
        while True:
            message = input("> ").strip()
            if message.lower() in {"/quit", "quit", "exit"}:
                print("Closing client...")
                break

            payload = json.dumps(message)
            await websocket.send(payload)
            response = await websocket.recv()
            print(f"[server] {response}")


if __name__ == "__main__":
    asyncio.run(run_client())
