import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect_to_server(server):
    addr = (server, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)

    return client


def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.sendall(send_length)
    client.sendall(message)

    response = client.recv(65535).decode(FORMAT)
    print(response, end="")


def main():
    server = input("Server IP: ")

    client = connect_to_server(server)

    try:
        while True:
            msg = input("> ")

            send(client, msg)

            if msg == DISCONNECT_MESSAGE:
                break
    finally:
        client.close()


if __name__ == "__main__":
    main()