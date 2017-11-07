#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(17, GPIO.OUT) ## Setup GPIO Pin 17 to OUT
GPIO.output(17,True) ## Turn on GPIO pin 17
time.sleep(2)
GPIO.output(17,False) ## Turn off GPIO pin 17
time.sleep(1)
GPIO.cleanup()
