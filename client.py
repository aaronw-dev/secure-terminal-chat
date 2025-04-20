import socketio
from time import sleep
import platform
from aiohttp import web
from datetime import datetime
import logging
import os
from colorama import Fore, Back, Style, init
import socketio.exceptions
from crpt import generatekey, encrypt, decrypt

init(autoreset=True)
size = os.get_terminal_size()
logging.basicConfig(level=logging.CRITICAL)
UIWidth = size.columns
messagelog = []

clientversion = "1.0.8"


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
    header = """ ___ _____ ___    ___ _ _         _
    / __|_   _/ __|  / __| (_)___ _ _| |_  
    \__ \ | || (__  | (__| | / -_) ' \  _|  
    |___/ |_| \___|  \___|_|_\___|_||_\__|  """
    for line in header.splitlines():
        print(headercolor + line.center(UIWidth))
    usernametext = f"username: {username}" if username != "" else ""
    print(
        headercolor
        + f"{usernametext}"
        + f"version {clientversion}".rjust(UIWidth - len(usernametext))
    )
    print(headercolor + "=" * UIWidth)


def printmessage(string):
    # now = datetime.now()
    # message = f"{Fore.YELLOW}[{now.strftime('%Y/%m/%d %H:%M:%S')}]{Fore.RESET} {string}"
    message = str(string)
    print(message)
    messagelog.append(message)


def refreshScreen():
    clear_terminal()
    sleep(0.1)
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


@client.event
def response(data):
    print(f"Response: {data}")


@client.event
def disconnect():
    printmessage(f"{Fore.RED}SERVER: DISCONNECTED FROM SERVER")


@client.on("welcome")
def welcome():
    printmessage("Connected to port 5000 on 127.0.0.1!")
    while True:
        try:
            metadata = {"username": username, "publickey": publickey}
            client.emit("metadata", metadata)
            break
        except socketio.exceptions.BadNamespaceError:
            sleep(0.5)
            continue


@client.on("usersupdate")
def usersupdate(data):
    global loggedusers
    loggedusers = data.copy()


@client.event
def message(data):
    message = data["message"]
    if data.get("encrypted"):
        if data["encrypted"] == True:
            message = decrypt(message, privatekey)
    if data["username"] == "SERVER":
        printmessage(f"{Fore.MAGENTA}{data['username']}: {message}")
    else:
        printmessage(f"{Fore.LIGHTGREEN_EX}{data['username']}{Fore.RESET}: {message}")
    refreshScreen()


def sendEncrypted(message, publickey, targetsid):
    cipher = encrypt(message, publickey)
    client.emit("message", {"message": cipher, "target": targetsid})


loggedusers = {}
username = ""
os.system(f"title Secure Terminal Chat Distributed Client v{clientversion}")
refreshScreen()
keybytes = 2048
print(f"{Fore.LIGHTMAGENTA_EX}Generating {keybytes} byte RSA key...")
privatekey, publickey = generatekey(keybytes)
print(f"{Fore.LIGHTMAGENTA_EX}RSA key successfully generated.")

while True:
    username = input("Enter username: ")
    if username != "":
        username = username.lower()
        username = username.strip()
        break

client.connect("http://127.0.0.1:5000")
while True:
    msg = input("")
    if msg.startswith("/"):
        print("invoking a command!")
        continue
    if client.connected and msg.strip() != "":
        for sid, usermeta in loggedusers.items():
            # printmessage(sid)
            sendEncrypted(msg, usermeta["publickey"], sid)

    else:
        refreshScreen()
