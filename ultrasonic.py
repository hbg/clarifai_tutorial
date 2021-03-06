import RPi.GPIO as GPIO
import time
import os
from glob import glob
from picamera import PiCamera
from PIL import Image, ImageDraw

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
TRAINING_ROOT = '/home/pi/clarifai_tutorial/training_us/'
map_values = []

def object_center(i):
    cam = PiCamera()
    cam.resolution = (500, 500)
    PATH = '/home/pi/clarifai_tutorial/captures/{}.jpg'.format(i)
    cam.capture(PATH)
    im = Image.open(PATH).convert('RGBA')
    id = ImageDraw.Draw(im)
    id.point([(250,250)], 0)
    im.save(PATH)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print(distance) 
    return distance
 
if __name__ == '__main__':
    try:
        while input('Record Distance?').lower()[0] == 'y':
            dist = distance()
            map_values.append(dist)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        i = len(glob(TRAINING_ROOT))
        print(i)
        f = open('{}{}.txt'.format(TRAINING_ROOT, str(i+1)), 'w+')
        f.write(str(map_values))
        f.close()
        object_center(str(i+1))
        GPIO.cleanup()
