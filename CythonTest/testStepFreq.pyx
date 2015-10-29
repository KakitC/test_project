""" Test max stepping speed and precision
"""
import math

__author__ = 'kakit'

import pyximport; pyximport.install()

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import time as time

# Import GPIO library, or fake version for development
try:
    print("Importing RPi.GPIO")
    import RPi.GPIO as GPIO
    print("Imported RPi.GPIO")
except ImportError:
    print("Main RPi.GPIO import failed, importing Fake RPI.GPIO instead")
    import FakeRPI.GPIO as GPIO
    print("FakeRPI.GPIO imported")


step_pin_a = 2
en_pin_a = 3
dir_pin_a = 4
mot_a_pins = (step_pin_a, en_pin_a, dir_pin_a)

cdef int dir_right = 0
cdef int dir_left = 1


def toggleFreq(int iters=100000):
#    Toggle GPIO stepper pins <iters> times and measure frequency

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(mot_a_pins, GPIO.OUT)

    #iters = 100000
    startTime = time()
    cdef int i
    for i in range(iters):
        GPIO.output(mot_a_pins, (True, True, dir_right))
        GPIO.output(mot_a_pins, (False, True, dir_right))
    deltaTime = time() - startTime
    print("Time to toggle " + str(iters) + " times: " + str(deltaTime))
    print("Toggle freq: " + str(iters / deltaTime))

    GPIO.cleanup()


def testJitter():
#    Track processor clock precision with GPIO toggles
#    what's the error on each call, accumulated error

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(mot_a_pins, GPIO.OUT)

    cdef double startTime = time()
    print startTime

    cdef double deltaTime = 0
    cdef int finishTime = 1
    cdef int iters = 10000  # iters = frequency if finishTime = 1
    cdef int count = 0
    cdef double saveTime[10000]

    while deltaTime < finishTime:
        deltaTime = time() - startTime

        if deltaTime > ((count + 1.0) * finishTime / iters):
            GPIO.output(mot_a_pins, (True, True, dir_right))
            GPIO.output(mot_a_pins, (False, True, dir_right))
            deltaTime = time() - startTime  # get new time value
            saveTime[count] = deltaTime
            count +=1

    print "Step iteration precision at {} counts in {}s, count: {}".format(iters, finishTime, count)
    print "i.e.{}/{}Hz".format(count / float(finishTime), iters / float(finishTime))

    errTime = [saveTime[x] - ((x+1.0) * finishTime / iters) for x in range(len(saveTime))]
    errTime = [0 if x < 0 else x for x in errTime]

    print "Ex. Errors, max, min: ", errTime[100:101], ", ", max(errTime), ", " , \
        min(errTime), "..."
    mean = sum(errTime) / count
    print "Average error: ", mean
    std_dev = math.sqrt(sum([(x - mean)**2 for x in errTime])/len(errTime))
    print "Standard deviation: ", std_dev

    GPIO.cleanup()
