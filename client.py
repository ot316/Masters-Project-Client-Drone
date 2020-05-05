import socket
import sys
import pickle 
import time
from dronekit import connect

# Connect to onboard MAVlink strean
ip = socket.gethostname()
vehicle = connect(ip, wait_ready=True)
# Use returned Vehicle object to query device state - e.g. to get the mode:
print("Mode: %s" % vehicle.mode.name)


#Ground server communication network configuration
port = 1234
ip = socket.gethostname()
HEADERSIZE = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((ip, port))
        print("connection established")
        break
    except ConnectionError as err:
        print('Connection error:', err)
        time.sleep(5)

class waypoint:
    def __init__(self,long,lat,alt):
        self.long = long
        self.lat = lat
        self.alt = alt
        
#await message
print("Waiting for message...")
while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("Command received")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print(b"raw command data:" + full_msg[HEADERSIZE:])
            data = pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b'' 
            print(data.alt)
            break

            
        
