import os
import asyncio
import aiohttp.web
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

async def index(request):
    return aiohttp.web.FileResponse(BASE_DIR / "index.html")

async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    print("WebSocket connection opened")
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Message from client: {msg.data}")
                await ws.send_str(f"Echo: {msg.data}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f"WebSocket connection closed with exception {ws.exception()}")
    finally:
        print("WebSocket connection closed")

    return ws

app = aiohttp.web.Application()
app.router.add_get("/", index)
app.router.add_get("/ws", websocket_handler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Render assigns PORT automatically
    aiohttp.web.run_app(app, host="0.0.0.0", port=port)
