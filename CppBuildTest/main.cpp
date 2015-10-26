/* 
 * File:   main.cpp
 * Author: kakit
 *
 * Created on October 21, 2015, 10:32 PM
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <bcm2835.h>
#include <sys/time.h>

#define PIN RPI_GPIO_P1_11
#define USEC_PER_SEC 1000000

long int timeDiff(timeval &start, timeval &end) {
    return (end.tv_sec - start.tv_sec)*USEC_PER_SEC 
		    + (end.tv_usec - start.tv_usec);
}

int main(int argc, char** argv) {
    struct timeval start, now;
    long int startTime;
    
    printf("Starting test...\n");
    
    //Init GPIO
    if (!bcm2835_init())
        return 1;
    // Set the pin to be an output
    bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);
    
//    //****************************************************************
//    printf("Max toggle frequency test");
//    //****************************************************************
//    int testIters = 1000 * 1000 * 10;
//    long int finishTime;
//    
//    gettimeofday(&start, NULL);
//    for (int i = 0; i < testIters; i++) {
//	bcm2835_gpio_write(PIN, HIGH);
//        bcm2835_gpio_write(PIN, LOW);
//    }
//    gettimeofday(&now, NULL);
//    finishTime = timeDiff(start, now);
//    printf("Time taken to toggle %d times: %dus\n", testIters, finishTime);
//    printf("Output frequency %fMHz\n\n", (double) testIters / (double) finishTime);
    
    
    //***************************************************************
    printf("GPIO jitter precision test");
    //***************************************************************
    long int deltaTime = 0;
    int testTime = 1 * USEC_PER_SEC;
    int targetFreq = 400; //Hz
    int targetPeriod = USEC_PER_SEC / targetFreq; //us
    int toggleIters = (int) ( ((double) targetFreq * USEC_PER_SEC) / (double) testTime );
    int saveTime[toggleIters];
    int count = 0;
    
    printf("testTime %d, targetFreq %d, targetPeriod %d, toggleIters %d\n",
	    testTime, targetFreq, targetPeriod, toggleIters);
    
    gettimeofday(&start, NULL);
    
    //Run test
    while (deltaTime < testTime) {
	gettimeofday(&now, NULL);
	deltaTime = timeDiff(start, now);
	
	//if (deltaTime > ((count + 1) * targetPeriod)) {
	if (deltaTime > (count * targetPeriod)) {
	    bcm2835_gpio_write(PIN, HIGH);
	    bcm2835_gpio_write(PIN, LOW);
	    bcm2835_gpio_write(PIN, HIGH);
	    bcm2835_gpio_write(PIN, LOW);
	    bcm2835_gpio_write(PIN, HIGH);
	    bcm2835_gpio_write(PIN, LOW);
	    bcm2835_gpio_write(PIN, HIGH);
	    bcm2835_gpio_write(PIN, LOW);
	    bcm2835_gpio_write(PIN, HIGH);
	    bcm2835_gpio_write(PIN, LOW);
	    
	    gettimeofday(&now, NULL);
	    deltaTime = timeDiff(start, now);
	    saveTime[count] = deltaTime;
	    count++;
	}
    }
    
    printf("Step iteration precision at %dHz in %dus, count: %d\n\n", 
	    targetFreq, testTime, count);
    
    //Get errors, and iterate to sum, max, and min the array
    int errTime[toggleIters];
    double meanErr = 0;
    int maxErr = 0;
    int minErr = testTime;
    int qosCutoff = 30;
    int qosCount = 0;
    for (int i = 0; i < toggleIters; i++) {
	errTime[i] = saveTime[i] - (i * targetPeriod);
	meanErr += errTime[i];
	if (errTime[i] > maxErr) maxErr = errTime[i];
	if (errTime[i] < minErr) minErr = errTime[i];
	if (errTime[i] > qosCutoff) qosCount++;
    }
    meanErr = meanErr / (double) toggleIters;
    
    long double stdDev = 0;
    for (int i = 0; i < toggleIters; i++) {
	stdDev += (long double) (errTime[i] - meanErr)*(errTime[i] - meanErr) / 
		(long double) toggleIters;
    }
    stdDev = sqrt(stdDev);
    
    printf("Err[0] %dus, Err[count] %dus, max %dus, min %dus\n", 
	    errTime[0], errTime[count-1], maxErr, minErr);
    printf("Mean Error %fus, Std Dev %fus, Err count above %dus %d\n", 
	    meanErr, stdDev, qosCutoff, qosCount);

    return (EXIT_SUCCESS);
}
