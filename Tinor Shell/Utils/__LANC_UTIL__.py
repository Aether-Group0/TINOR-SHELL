from Utils.__LAN_CHAT__.__LANC_SERVER__ import start
from Utils.__LAN_CHAT__.__LANC_CLIENT__ import send, DISCONNECT_MESSAGE


def send_handling(command_input):
    while True:
        msg = input("> ")

        send(msg)

        if msg == DISCONNECT_MESSAGE:
            break


def Startff(command_input):
    print("[TCP SERVER STARTING] Starting TCP server...")
    start()