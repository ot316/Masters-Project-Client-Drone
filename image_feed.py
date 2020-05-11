from time import sleep
from picamera import PiCamera

camera = PiCamera()

while true:
    i += 1
    camera.capture(f'.//flight_images/{i}.jpg')
    sleep(0.5)
