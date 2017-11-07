#!/usr/bin/env python

import sys, os
sys.path.append(os.path.dirname(__file__) + "/../")

import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
from ElectronicComponents import SevenDigits

# port for stop button
STOP_BUTTON = 21

def init_electronic():
    GPIO.setmode(GPIO.BCM)
    # Input reset (stop)
    GPIO.setup(STOP_BUTTON, GPIO.IN)  ## stop button

def main():

    #init electronic components
    init_electronic()

    port_digits = (19, 26, 22, 27, 18, 13, 06, 17)
    seven_digits = SevenDigits( port_digits )
    
    # switch on "dc" light
    seven_digits.set_light_on("dc")

    # rotation for test
    stopLoop = False
    while not stopLoop:
        stopLoop = GPIO.input(STOP_BUTTON)

        for i in range(97, 103):
            entry = chr(i)
            print(entry)
            seven_digits.set_light_on(entry)
            time.sleep(0.05)
            seven_digits.set_light_off(entry)

    time.sleep(0.5)

    # count down
    for i in range(9,-1,-1):
        print(i)
        seven_digits.write_output(str(i))
        time.sleep(1)

    for i in range(97,103):
        print(chr(i))
        seven_digits.write_output(chr(i))
        time.sleep(1)

    for i in range(97,103):
        print(i)
        seven_digits.write_output(i)
        time.sleep(1)
        

    # clean seven digits
    seven_digits.clean(clean_dc = True)

    # clean the GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
   
