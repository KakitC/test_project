""" Measure CPU clock speed and precision
"""
import math

__author__ = 'kakit'

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import time as time
    
# Count how many times I can call something in 1ms
# Raw time() call speed: 3500/ms
# With other stuff: 2500/ms
# With 1 print statement: 200/ms
startTime = time()
deltaTime = 0
count = 0
while deltaTime < .001:
    deltaTime = time() - startTime
    count += 1
    #print deltaTime
    #print count
print "Iterations in 1ms ", count #with print statement: ", count

# Track processor clock precision,
# what's the error on each call at 1us period, accumulated error
startTime = time()
deltaTime = 0
finishTime = 1
iters = 4000
count = 0
saveTime = []
while deltaTime < finishTime: # less than 1ms
    deltaTime = time() - startTime
    if deltaTime > ((count + 1.0) * finishTime / iters):
        count +=1
        saveTime.append(deltaTime)

print "Iteration precision at {} counts in {}s, count: {}".format(iters, finishTime, count)
print "i.e.{}/{}Hz".format(count / float(finishTime), float(iters) / finishTime)

errTime = [saveTime[x] - ((x + 1.0) * float(finishTime) / iters) for x in range(len(saveTime))]

print "Ex. Errors, max, min: ", errTime[100:101], ", ", max(errTime), ", " , \
    min(errTime), "..."
mean = sum(errTime) / count
print "Average error: ", mean
std_dev = math.sqrt(sum([(x - mean)**2 for x in errTime])/len(errTime))
print "Standard deviation: ", std_dev
print "dev: ", [x - mean for x in errTime[100:105]]