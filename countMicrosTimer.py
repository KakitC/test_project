""" Measure CPU clock speed and precision
"""

__author__ = 'kakit'

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import clock as time
    
# Count how many times I can call something in 1ms
# Raw time() call speed: 3500/ms
# With other stuff: 2500/ms
# With 1 print statement: 200/ms
deltaTime = time()
count = 0
while deltaTime < .001:
    deltaTime = time()
    count += 1
    print deltaTime
    print count
print "Iterations in 1ms with print statement: ", count

# Track processor clock precision,
# what's the error on each call at 1us period, accumulated error
startTime = time()
deltaTime = 0
iters = 800
count = 0
saveTime = []
while deltaTime < .001: # less than 1ms
    deltaTime = time() - startTime
    if deltaTime > ((count + 1) / 1000.0 / iters):
        count +=1
        saveTime.append(deltaTime)
print "Iteration precision at 1000 counts in 1ms, count: ", count
errTime = [saveTime[x] - ((x +1) / 1000.0 / iters) for x in range(len(saveTime))]
print "Errors: ", errTime[0:10]
print "Average error: ",  sum(errTime) / count
