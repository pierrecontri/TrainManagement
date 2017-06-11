#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.realpath("ElectronicComponents"))
sys.path.append(os.path.realpath("ElectronicModel"))

import time ## Import 'time' library. Allows us to use 'sleep'
from ElectronicComponents import *
from ElectronicModel import Chase

def chase_demo():

    #init electronic components
    InitGPIO.init_electronic()

    stop_button = StopButton(21)
    eight_outputs = SN74HC595( {'ser':5,'oe':6,'rclk':13,'srclk':19,'srclr':26} )
    chase = Chase()
    print("Chase ON")

    eight_outputs.allow_output(True)

    while not stop_button.stop_state:
        eight_outputs.write_output( chase.ticks() )
        time.sleep(0.05)

    eight_outputs.write_output( 128 )
    time.sleep(2)
    print("Chase OFF")

    # clean the GPIO
    InitGPIO.clean()


if __name__ == '__main__':
    try:
        chase_demo()
    except KeyboardInterrupt:
        InitGPIO.clean()
    
