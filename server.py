import asyncio
import websockets
import json

led_state = "OFF"
clients = set()

async def handler(websocket):
    global led_state
    clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "toggle":
                    led_state = data.get("state", "OFF")
                    print(f"LED set to {led_state}")
                    await asyncio.gather(
                        *[ws.send(json.dumps({"type": "state", "state": led_state})) for ws in clients]
                    )
                elif data.get("type") == "get_state":
                    await websocket.send(json.dumps({"type": "state", "state": led_state}))
            except json.JSONDecodeError:
                print("Invalid message:", message)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 5000):
        print("WebSocket server running at ws://0.0.0.0:5000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
