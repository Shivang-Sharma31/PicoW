import os
import asyncio
import json
from aiohttp import web

PORT = int(os.environ.get("PORT", 8000))
HOST = "0.0.0.0"

# LED state variable
led_state = "OFF"

# HTTP handler
async def http_handler(request):
    return web.Response(text="OK")

# WebSocket handler
async def ws_route_handler(request):
    global led_state
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("WebSocket connected")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except json.JSONDecodeError:
                continue

            if data.get("type") == "get_state":
                await ws.send_str(json.dumps({"type": "state", "state": led_state}))

            elif data.get("type") == "toggle":
                led_state = data.get("state", led_state)
                await ws.send_str(json.dumps({"type": "state", "state": led_state}))

    print("WebSocket closed")
    return ws

async def main():
    app = web.Application()
    app.router.add_get("/", http_handler)
    app.router.add_get("/ws", ws_route_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    print(f"Server running on {HOST}:{PORT}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
