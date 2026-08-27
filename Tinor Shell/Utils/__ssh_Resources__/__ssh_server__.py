import socket
import threading
import subprocess

#Variables
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#Handle Clients function
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
                
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False


            sent_Command = subprocess.run(
        msg,
        shell=True,
        capture_output=True,
        text=True
        )
            output = sent_Command.stdout + sent_Command.stderr


            print(f"[{addr}] {msg}")
            conn.send(output.encode(FORMAT))

    conn.close()

#Start Function
def start():
    PORT = 5050
    SERVER = input("Enter Your Public IP:")
    ADDR = (SERVER, PORT)
    
    #Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
