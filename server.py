import socketio
from aiohttp import web
from datetime import datetime
import logging
import os

size = os.get_terminal_size()

logging.getLogger("aiohttp.server").setLevel(logging.CRITICAL)

UIWidth = 56
print("=" * UIWidth)
print("STC (Secure Terminal Chat) Server".center(UIWidth))
print("=" * UIWidth)


def serverPrint(string):
    now = datetime.now()
    print(f"[{now.strftime('%Y/%m/%d %H:%M:%S')}] {string}")


async def sendMessage(string):
    await server.emit("message", {"data": string})


serverPrint("Initializing messaging server...")
server = socketio.AsyncServer(cors_allowed_origins="*")  # ,logger=True)
app = web.Application()
server.attach(app)

serverPrint("Creating server bindings...")


@server.event
async def connect(sid, environ):
    serverPrint(f"USER [{sid}] CONNECTED.")
    await sendMessage(f"USER [{sid}] CONNECTED.")


@server.event
async def disconnect(sid):
    serverPrint(f"USER [{sid}] DISCONNECTED.")
    await sendMessage(f"USER [{sid}] DISCONNECTED.")


@server.event
async def message(sid, data):
    serverPrint(f"{sid}: {data['data']}")


serverPrint("Starting messaging server...")
web.run_app(app, port=5000, access_log=None)
