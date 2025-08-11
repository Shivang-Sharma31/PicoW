import os
import asyncio
from aiohttp import web

PORT = int(os.environ.get("PORT", 8000))
HOST = "0.0.0.0"

# --- Serve index.html ---
async def index(request):
    return web.FileResponse("index.html")

# --- WebSocket handler ---
async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("WebSocket connected")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print(f"Received: {msg.data}")
            await ws.send_str(f"Echo: {msg.data}")
    print("WebSocket closed")
    return ws

# --- App setup ---
def create_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", ws_handler)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host=HOST, port=PORT)
