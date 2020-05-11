from dronekit import connect, VehicleMode, LocationGlobal, Command, LocationGlobalRelative
from pymavlink import mavutil
import sys

def arm_and_roll():
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Pseudo Takeoff")
    vehicle.simple_takeoff(1)  # Take off but not leave the ground
    time.sleep(4)
    

def arm_and_takeoff(tgt_altitude):
    print("Arming motors")
    
    while not vehicle.is_armable:
        time.sleep(1)
        
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed: time.sleep(1)
    
    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)
    
    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt
        
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break
            
        time.sleep(1)
        

def finish_mission():
    #arm_and_takeoff(5)
    vehicle.mode = VehicleMode("RTL")  
    position = vehicle.locationlocal
    if abs(position.north) < 2 and abs(position.east) < 2: #if drone is within 2 meters of origin
        print ("Home position reached")
        vehicle.mode = VehicleMode("land")
        print("landing")
        if position.down < -0.2: # if drone is 20cm above the ground
            vehicle.armed = False
            print("Vehicle disarmed, mission completed")
            sys.exit()
        
