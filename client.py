import socketio

client = socketio.Client()  # logger=True)


@client.event
def connect():
    print("Connected to server.")


@client.event
def response(data):
    print(f"Response: {data}")


@client.event
def disconnect():
    print("Disconnected from server.")


@client.event
def message(data):
    print(f"> {data['data']}")


client.connect("http://0.0.0.0:5000")
while True:
    msg = input("> ")
    client.emit("message", {"data": msg})
