import socket
import sys

port = 1234
ip = socket.gethostname()
HEADERSIZE = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length : {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full message received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''

    print(full_msg)
    sys.exit()
