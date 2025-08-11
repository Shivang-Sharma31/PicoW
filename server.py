import os
import asyncio
import websockets

PORT = int(os.environ.get("PORT", 10000))  # Render sets PORT env var

async def handler(websocket):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Server running on port {PORT}")
        await asyncio.Future()  # run forever

asyncio.run(main())
