""" Test max stepping speed and precision
"""

__author__ = 'kakit'

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import time as time

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

GPIO.setmode(GPIO.BCM)
GPIO.setup(mot_a_pins, GPIO.OUT)

# Toggle GPIO stepper pins <iters> times
iters = 100000
startTime = time()
for i in range(iters):
    GPIO.output(mot_a_pins, (True, True, dir_right))
    GPIO.output(mot_a_pins, (False, True, dir_right))
endTime = time()
print("Time to toggle " + str(iters) + " times: " + str(endTime - startTime))


# Track processor clock precision with GPIO toggles
# what's the error on each call, accumulated error
startTime = time()
print startTime
deltaTime = 0
finishTime = 1
iters = 20000  # iters = frequency if finishTime = 1
count = 0
saveTime = []
while deltaTime < finishTime:
    deltaTime = time() - startTime

    if deltaTime > ((count + 1.0) * finishTime / iters):
        GPIO.output(mot_a_pins, (True, True, dir_right))
        GPIO.output(mot_a_pins, (False, True, dir_right))
        count +=1
        deltaTime = time() - startTime  # get new time value
        saveTime.append(deltaTime)

print "Step iteration precision at {} counts in {}s, count: {}".format(iters, finishTime, count)
print "i.e.{}/{}Hz".format(count / float(finishTime), iters / float(finishTime))

errTime = [saveTime[x] - ((x+1.0) * finishTime / iters) for x in range(len(saveTime))]
print "delta: ", saveTime[100:105]
print "Errors: ", errTime[100:105], "..."
print "Average error: ",  sum(errTime) / count


GPIO.cleanup()
