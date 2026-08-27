import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect_to_server(server):
    ADDR = (server, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    return client


def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))


if __name__ == "__main__":
    SERVER = input("ENTER PUBLIC IP: ")

    client = connect_to_server(SERVER)

    while True:
        msg = input("> ")

        if msg == DISCONNECT_MESSAGE:
            send(client, msg)
            break

        send(client, msg)