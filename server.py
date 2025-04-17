from time import sleep
import socketio
from aiohttp import web
from datetime import datetime
import logging
import os
import asyncio
from colorama import Fore, Back, Style, init

init(autoreset=True)

size = os.get_terminal_size()

logging.basicConfig(level=logging.CRITICAL)

UIWidth = size.columns

messagelog = []


def printHeader():
    print(Fore.RED + "=" * UIWidth)
    # print("STC (Secure Terminal Chat) Server".center(UIWidth))
    header = """   ___ _____ ___   ___                      
  / __|_   _/ __| / __| ___ _ ___ _____ _ _ 
  \__ \ | || (__  \__ \/ -_) '_\ V / -_) '_|
 |___/ |_| \___| |___/\___|_|  \_/\___|_|"""
    for line in header.splitlines():
        print(Fore.WHITE + line.center(UIWidth))
    print("version 1.0.1".rjust(UIWidth))
    print(Fore.RED + "=" * UIWidth)


def serverPrint(string):
    now = datetime.now()
    message = f"[{now.strftime('%Y/%m/%d %H:%M:%S')}] {string}"
    print(message)
    messagelog.append(message)


def refreshScreen():
    os.system("clear")
    printHeader()
    logs = messagelog.copy()
    if len(logs) > size.lines - 7:
        logs = messagelog[len(logs) - size.lines - 7 :]
    for message in logs:
        print(message)


async def sendMessage(string, sid="SERVER"):
    await server.emit("message", {"sid": sid, "data": string})


serverPrint("Initializing messaging server...")
server = socketio.AsyncServer(
    cors_allowed_origins="*", async_mode="aiohttp"
)  # ,logger=True)
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
    data["sid"] = sid
    serverPrint(f"{sid}: {data['data']}")
    await server.emit("message", data)
    refreshScreen()


async def start_server():
    os.system("clear")
    printHeader()
    serverPrint("Starting messaging server...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=5000)
    await site.start()

    serverPrint("Messaging server booted!")
    refreshScreen()

    while True:
        await asyncio.sleep(3600)  # Keep it alive


asyncio.run(start_server())
