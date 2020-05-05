from dronekit import connect, VehicleMode, LocationGlobal, Command, LocationGlobalRelative
import pandas as pd
import socket
import time

def collectdata():
    time = datetime.now()
    volts = vehicle.battery.voltage
    current = vehicle.battery.current
    speed = vehicle.groundspeed
    long = vehicle.location_relative_frame.long
    lat = vehicle.location_relative_frame.lat
    alt = vehicle.location_relative_frame.alt
    
    
# Connect to onboard MAVlink strean
ip = socket.gethostname()
vehicle = connect(ip, wait_ready=True)
print("Connection to MAVlink established")
data = []

while vehicle.armed == False:
    print("waiting for vehicle to arm")
    time.sleep(1)

while vehicle.armed:
    ("Vehicle armed, data logging initialised")
    for time, volts, amps, speed, long, lat, alt in collectdata():
        data.append([time, volts, amps, speed, long, lat, alt])
        time.sleep(1)
    
column_names = ["Time", "Battery Voltage", "Battery Current", "Ground Speed", "longitude", "Latitude", "altitude"]
df = pd.DataFrame(data, columns = column_names)
df.to_csv('flight_data_log.csv')