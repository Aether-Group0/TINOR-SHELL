from Utils.__ssh_Resources__.__ssh_client__ import send
from Utils.__ssh_Resources__.__ssh_server__ import start


def START_SERVER():
   start()

def Messaging_system():
    while True:
     msg = input()
     send(msg)