import os
import asyncio
from aiohttp import web

# Store LED state in memory (for simplicity)
led_state = {"status": "off"}
clients = set()

# WebSocket handler
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)

    # Send current state to new client
    await ws.send_json(led_state)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = msg.json()
            # Update LED state
            if "status" in data:
                led_state["status"] = data["status"]

                # Broadcast to all clients
                for client in clients:
                    if not client.closed:
                        await client.send_json(led_state)

        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket connection closed with exception {ws.exception()}")

    clients.remove(ws)
    return ws

# HTTP handler (serves HTML file)
async def index_handler(request):
    return web.FileResponse("templates/index.html")

# Create app
app = web.Application()
app.router.add_get("/", index_handler)
app.router.add_get("/ws", websocket_handler)
app.router.add_static("/static", "static")  # if you have CSS/JS

# Render uses dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    web.run_app(app, host="0.0.0.0", port=port)
