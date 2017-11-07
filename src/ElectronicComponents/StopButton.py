#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library

class StopButton(object):

    def __init__(self, port_button):
        self.port = port_button
        GPIO.setwarnings(False)
        # Input reset (stop)
        GPIO.setup(self.port, GPIO.IN)  ## stop button
        
    @property
    def stop_state(self):
        return GPIO.input(self.port)
    
