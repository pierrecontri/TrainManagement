#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library

class InitGPIO(object):

    @staticmethod
    def init_electronic():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    @staticmethod
    def clean():
        GPIO.cleanup()
