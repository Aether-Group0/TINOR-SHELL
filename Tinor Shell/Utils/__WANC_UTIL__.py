from Utils.__WAN_CHAT__.__WAN_SERVER__ import start
from Utils.__WAN_CHAT__.__WANC_CLIENT__ import send, DISCONNECT_MESSAGE


def send_handling_W(Command_input):
    while True:
        msg = input("> ")

        send(msg)

        if msg == DISCONNECT_MESSAGE:
            break


def Startff_W(Command_input):
    print("[STARTING]")
    start("WAN server has started")