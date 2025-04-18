import platform
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
clientversion = "1.0.4"
loggedusers = {"SERVER": {"username": "SERVER"}}


def clear_terminal():
    """Clears the terminal screen on any platform."""
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def printHeader():
    print(Fore.GREEN + "=" * UIWidth)
    # print("STC (Secure Terminal Chat) Server".center(UIWidth))
    header = """   ___ _____ ___   ___                      
  / __|_   _/ __| / __| ___ _ ___ _____ _ _ 
  \__ \ | || (__  \__ \/ -_) '_\ V / -_) '_|
 |___/ |_| \___| |___/\___|_|  \_/\___|_|"""
    for line in header.splitlines():
        print(Fore.GREEN + line.center(UIWidth))
    print(Fore.GREEN + f"version {clientversion}".rjust(UIWidth))
    print(Fore.GREEN + "=" * UIWidth)


def serverPrint(string):
    now = datetime.now()
    message = f"{Fore.YELLOW}[{now.strftime('%Y/%m/%d %H:%M:%S')}]{Fore.RESET} {string}"
    print(message)
    messagelog.append(message)


def refreshScreen():
    clear_terminal()
    printHeader()
    logs = messagelog.copy()
    logthreshold = size.lines - 8
    overflow = len(logs) - logthreshold
    # print("length: " + str(len(logs)))
    # print("threshold: " + str(logthreshold))
    # print("overflow: " + str(overflow))
    if overflow >= 0:
        logs = messagelog[-logthreshold:]
    for message in logs:
        print(message)


async def sendMessage(string, sid="SERVER"):
    # await server.emit("message", {"sid": sid, "data": string})
    await server.emit("message", {"sid": sid, "data": string, "username": loggedusers[sid]["username"]})


serverPrint(f"{Fore.LIGHTBLUE_EX}Initializing messaging server...")
server = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="aiohttp"
)  # ,logger=True)
app = web.Application()
server.attach(app)

serverPrint(f"{Fore.LIGHTBLUE_EX}Creating server bindings...")


@server.event
async def connect(sid, environ):
    await server.emit("welcome", to=sid)


@server.on("metadata")
async def receivemetadata(sid, data):
    username = data["username"]
    loggedusers[sid] = {"username": username}
    serverPrint(f"{Fore.MAGENTA}USER [{username.upper()}]({sid}) CONNECTED.")
    await sendMessage(f"USER [{username.upper()}]({sid}) CONNECTED.")


@server.event
async def disconnect(sid):
    usermetadata = loggedusers[sid]
    username = usermetadata["username"].upper()
    serverPrint(f"{Fore.MAGENTA}USER [{username}]({sid}) DISCONNECTED.")
    await sendMessage(f"USER [{username}]({sid}) DISCONNECTED.")


@server.event
async def message(sid, data):
    data["sid"] = sid
    data["username"] = loggedusers[sid]["username"]
    serverPrint(f"{loggedusers[sid]['username']}: {data['data']}")
    await server.emit("message", data)
    refreshScreen()


async def start_server():
    os.system(f"title Secure Terminal Chat Server v{clientversion}")
    clear_terminal()
    printHeader()
    serverPrint(f"{Fore.LIGHTBLUE_EX}Starting messaging server...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=5000)
    await site.start()

    serverPrint(f"{Fore.LIGHTBLUE_EX}Messaging server booted!")
    refreshScreen()

    while True:
        await asyncio.sleep(3600)  # Keep it alive


asyncio.run(start_server())
