from dronekit import connect, VehicleMode, LocationLocal
from pymavlink import mavutil
from utils import arm_and_roll, arm_and_takeoff, finish_mission
#import picamera.array
import numpy, cv2, time, pickle, sys, socket, picamera

#set up camera
camera = PiCamera()
camera.rotation = 180

class data_return:
    def __init__(self, image, location, volts):
        self.image = image
        self.location = location
        self.volts = volts

# Connect to onboard MAVlink strean
ip = socket.gethostname()
vehicle = connect(ip, wait_ready=True)
print("Conencted to MAVlink, Mode: %s" % vehicle.mode.name)


#Ground server communication network configuration
SERVER_PORT = 1234
SERVER_IP = socket.gethostname() #temporary, replace with real IP
HEADERSIZE = 20


#parameters for mission
disconnect_timeout = 60*5

seconds_disconnected = 0

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                #print(b"raw command data:" + full_msg[HEADERSIZE:])
                data = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b'' 
                break
    
        if data.down == 'finish mission':
            print("mission complete")
            finish_mission()
            
            
            
        #reduce maximum motor speed to prevent takeoff and force rolling
        vehicle.parameters['MOT_SPIN_MAX'] = 0.3
        arm_and_roll()
        
        #sert rolling speed
        vehicle.airspeed = 3
        
        print ("roll to received waypoint")
        
        while True: 
            position = vehicle.locationlocal
            vehicle.simple_goto(data)
            if abs(position.north - data.north) < 0.1 * data.north:
                if abs(position.east - data.east) < 0.1 * data.east:
                    print ("waypoint reached")
                    break
        
        #set flight mode
        vehicle.parameters['MOT_SPIN_MAX'] = 0.95
        #Take off
        arm_and_takeoff(data.down)
        
        #take picture
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb')
            i = i+1
            cv2.imwrite(f'image_at_waypoint_{i}.png', output)
        
        #land
        vehicle.mode = VehicleMode("land")   
        
        #send photo, location and battery back to server
        data = data_return(image, position, vehicle.battery.voltage)
        bytes_data = pickle.dumps(data)
        msg = bytes(f'{len(bytes_data):<{HEADERSIZE}}', "utf-8") + bytes_data
        s.send(msg)
        print("Data sent to server")
        break
    




    
            
        
