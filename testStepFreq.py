""" Test max stepping speed and precision
"""

__author__ = 'kakit'

import time

# Import GPIO library, or fake version for development
try:
    import RPi.GPIO as GPIO
    print("Real RPi.GPIO imported")
except ImportError:
    print("Importing Fake RPI.GPIO")
    import FakeRPI.GPIO as GPIO

# Import picamera library, or fake version for development
try:
    import picamera as pic
    print("Real RPi.GPIO imported")
except ImportError:
    import FakePicamera as pic
    print("Importing Fake picamera")

step_pin_a = 1
en_pin_a = 2
dir_pin_a = 3
mot_a_pins = (step_pin_a, en_pin_a, dir_pin_a)

dir_right = 0
dir_left = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(step_pin_a, GPIO.OUTPUT)

# Toggle GPIO stepper pins <iters> times
iters = 1000000
startTime = time.clock()
for i in range(iters):
    GPIO.output(mot_a_pins, (True, True, dir_right))
    GPIO.output(mot_a_pins, (False, True, dir_right))
endTime = time.clock()
print("Time to toggle " + str(iters) + " times: " + str(endTime - startTime))



GPIO.cleanup()