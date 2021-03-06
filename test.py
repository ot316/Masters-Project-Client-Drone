from dronekit import connect, VehicleMode, LocationLocal
from pymavlink import mavutil
from utils import arm_and_roll, arm_and_takeoff, finish_mission
#import picamera.array
import numpy, cv2, time, pickle, sys, socket



class data_return:
    def __init__(self, image, location, volts):
        self.image = image
        self.location = location
        self.volts = volts


#Ground server communication network configuration
SERVER_PORT = 1234
SERVER_IP = socket.gethostname() #temporary, replace with real IP
HEADERSIZE = 20
        
        
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #parameters for mission
    disconnect_timeout = 60*5
    
    seconds_disconnected = 0
    while True:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print("connection established")
            break
        except ConnectionError as err:
            print('Connection error:', err)
            time.sleep(5)
            seconds_disconnected = seconds_disconnected + 5
            if seconds_disconnected > disconnect_timeout:
                print(f"No Connection for {disconnect_timeout} secondes, returning to launch")
                #reduce maximum motor speed to prevent takeoff and force rolling
                vehicle.parameters['MOT_SPIN_MAX'] = 0.3
                finish_mission()
                
                    
    #await message
    i = 0
    while True:
        print("Waiting for message...")
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
                #print(b"raw command data:" + full_msg[HEADERSIZE:])
                data = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b'' 
                break
    
        if data == 'finish_mission':
            print("mission complete")
            sys.exit()         
    
        
        print (f"roll to received waypoint x = {data.east} y = {data.north}")
        
        #while True: 
            #position = vehicle.locationlocal
            #vehicle.simple_goto(data)
            #if abs(position.north - data.north) < 0.1 * data.north:
                #if abs(position.east - data.east) < 0.1 * data.east:
                    #print ("waypoint reached")
                    #break
        time.sleep(2)
    
        
        #send photo, location and battery back to server
        #data = data_return(image, position, vehicle.battery.voltage)
        data = data_return(10, 100, 50)   
        bytes_data = pickle.dumps(data)
        msg = bytes(f'{len(bytes_data):<{HEADERSIZE}}', "utf-8") + bytes_data
        s.send(msg)
        print("Data sent to server")
        break




    
            
        
