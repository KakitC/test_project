""" Test max stepping speed and precision
"""

__author__ = 'kakit'

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import clock as time

# Import GPIO library, or fake version for development
try:
    import RPi.GPIO as GPIO
    print("Real RPi.GPIO imported")
except ImportError:
    print("Importing Fake RPI.GPIO")
    import FakeRPI.GPIO as GPIO


step_pin_a = 2
en_pin_a = 3
dir_pin_a = 4
mot_a_pins = (step_pin_a, en_pin_a, dir_pin_a)

dir_right = 0
dir_left = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(step_pin_a, GPIO.OUTPUT)

# Toggle GPIO stepper pins <iters> times
iters = 1000000
startTime = time()
for i in range(iters):
    GPIO.output(mot_a_pins, (True, True, dir_right))
    GPIO.output(mot_a_pins, (False, True, dir_right))
endTime = time()
print("Time to toggle " + str(iters) + " times: " + str(endTime - startTime))



GPIO.cleanup()