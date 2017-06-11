#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) ## Setup GPIO Pin 17 to OUT

##Define a function named Blink()
def Blink(numTimes,speed):
    for i in range(0,numTimes):## Run loop numTimes
        print "Iteration " + str(i+1)## Print current loop
        GPIO.output(17,True)## Switch on pin 17
        time.sleep(speed)## Wait
        GPIO.output(17,False)## Switch off pin 17
        time.sleep(speed)## Wait in seconds
    print "Done" ## When loop is complete, print "Done"


## Ask user for total number of blinks and length of each blink
iterations = raw_input("Enter total number of times to blink: ")
speed = raw_input("Enter length of each blink(seconds): ")

## Start Blink() function. Convert user input from strings to numeric data types and pass to Blink() as parameters
Blink(int(iterations),float(speed))

GPIO.cleanup()
