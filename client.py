import socketio
from time import sleep
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

clientversion = "1.0.5"


def moveCursor(y, x):
    print("\033[%d;%dH" % (y, x), end="")


def clear_terminal():
    """Clears the terminal screen on any platform."""
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def printHeader():
    headercolor = Fore.CYAN
    print(headercolor + "=" * UIWidth)
    # print("STC (Secure Terminal Chat) Server".center(UIWidth))
    header = """  ___ _____ ___    ___ _ _         _   
 / __|_   _/ __|  / __| (_)___ _ _| |_ 
 \__ \ | || (__  | (__| | / -_) ' \  _|
 |___/ |_| \___|  \___|_|_\___|_||_\__|"""
    for line in header.splitlines():
        print(headercolor + line.center(UIWidth))
    print(headercolor + f"version {clientversion}".rjust(UIWidth))
    print(headercolor + "=" * UIWidth)


def printmessage(string):
    # now = datetime.now()
    # message = f"{Fore.YELLOW}[{now.strftime('%Y/%m/%d %H:%M:%S')}]{Fore.RESET} {string}"
    message = string
    if (message.startswith("SERVER: ")):
        message = Fore.MAGENTA + message
    print(message)
    messagelog.append(message)


def refreshScreen():
    clear_terminal()
    printHeader()
    logs = messagelog.copy()
    logthreshold = size.lines - 9
    overflow = len(logs) - logthreshold
    if overflow >= 0:
        logs = messagelog[-logthreshold:]
    for message in logs:
        print(message)
    moveCursor(size.lines, 1)


client = socketio.Client()  # logger=True)


# @client.event
# def connect():
#    print("Connected to server.")


@client.event
def response(data):
    print(f"Response: {data}")


@client.event
def disconnect():
    print("Disconnected from server.")


@client.event
def message(data):
    printmessage(f"{data['sid']}: {data['data']}")
    refreshScreen()


os.system(f"title Secure Terminal Chat Distributed Client v{clientversion}")
client.connect("http://127.0.0.1:5000")
while True:
    msg = input("")
    client.emit("message", {"data": msg})
