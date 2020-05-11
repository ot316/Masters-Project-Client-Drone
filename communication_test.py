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

#parameters for mission
disconnect_timeout = 60*5
seconds_disconnected = 0
i = 1

while True:  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        break
    
    except:
        print("Connection rejected, retrying...")
        if seconds_disconnected > disconnect_timeout:
            print(f"No Connection for {disconnect_timeout} secondes, returning to launch")
            time.sleep(5)
            seconds_disconnected = seconds_disconnected + 5            
            #reduce maximum motor speed to prevent takeoff and force rolling
            vehicle.parameters['MOT_SPIN_MAX'] = 0.3
            finish_mission()      
        
while True:        
    #await message
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
                data = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                print(data)
                if data == 'end_mission':
                    print("mission complete")
                    sys.exit()                   
                full_msg = b'' 
                break
            
      
    
        
        print (f"roll to received waypoint x={data.east} y={data.north}")
        
        #while True: 
            #position = vehicle.locationlocal
            #vehicle.simple_goto(data)
            #if abs(position.north - data.north) < 0.1 * data.north:
                #if abs(position.east - data.east) < 0.1 * data.east:
                    #print ("waypoint reached")
                    #break
        time.sleep(1.5)
        print("taking picture...")
        time.sleep(2)
    
        
        #send photo, location and battery back to server
        #data = data_return(image, position, vehicle.battery.voltage)
        image = cv2.imread(f'.//test_images/{i}.png',1)     
        data = data_return(image, 100, 50)   
        time.sleep(1)
        bytes_data = pickle.dumps(data)
        msg = bytes(f'{len(bytes_data):<{HEADERSIZE}}', "utf-8") + bytes_data
        s.send(msg)
        print("Data sent to server")
        time.sleep(1)
        i += 1
        break




    
            
        
