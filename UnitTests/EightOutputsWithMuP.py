#!/usr/bin/env python

import sys, os
sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("../ElectronicComponents"))
sys.path.append(os.path.realpath("../ElectronicModel"))

import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
from ElectronicComponents import *
from ElectronicModel import Chase

# port for stop button
STOP_BUTTON = 21

def init_electronic():
    GPIO.setmode(GPIO.BCM)
    # Input reset (stop)
    # in the StopButton constructor
    #GPIO.setup(STOP_BUTTON, GPIO.IN)  ## stop button

    # init seven digits
    # in the seven_digits constructor

    # init the SN74HC959inputs
    # in the SN74HC595 constructor
    
def main():

    #init electronic components
    InitGPIO.init_electronic()

    stop_button = StopButton(STOP_BUTTON)

    eight_outputs = SN74HC595( {'ser':5,'oe':6,'rclk':13,'srclk':19,'srclr':26} )

    chase = Chase()

    eight_outputs.allow_output(True)

    while not stop_button.stop_state:
        ti = chase.ticks()
        print(ti)
        eight_outputs.write_output( ti )
        time.sleep(0.2)

    eight_outputs.write_output( 128 )
    time.sleep(2)

    # clean the GPIO
    InitGPIO.clean()

def main3():

    #init electronic components
    init_electronic()

    eight_outputs = SN74HC595( {'ser':5,'oe':6,'rclk':12,'srclk':19,'srclr':26} )
    seven_digits_1 = SevenDigits( (19, 26, 22, 27, 18, 13, 6, 17) )
    seven_digits_2 = SevenDigits(output_ports = None, use_direct_gpio = False, component_interface = eight_outputs)

    chase = Chase()
    dummyChase = True

    objectOutput = None

    eight_outputs.allow_output(True)

    i = 0

    # step 1
    seven_digits_1.set_light_on("dc")
    seven_digits_2.set_light_off("dc")
    while not GPIO.input(STOP_BUTTON):
        output_mod1 = str(hex(i % 16))[-1]
        output_mod2 = str(hex((i / 16) % 16))[-1]

        #seven_digits_1.write_output( output_mod1 )
        if dummyChase:
            eight_outputs.write_output( chase.ticks() )
        else:
            seven_digits_2.write_output( output_mod2 )

        i += 1
        time.sleep(0.2)

    time.sleep(2)

    # step 2
    seven_digits_1.set_light_off("dc")
    seven_digits_2.set_light_on("dc")
    seven_digits_1.write_output("2")
    while not GPIO.input(STOP_BUTTON):
        for j in range(97, 103):
            seven_digits_2.write_output( chr(j) )
            time.sleep(0.2)

    time.sleep(2)

    # step 3
    seven_digits_1.set_light_on("dc")
    seven_digits_2.set_light_on("dc")
    seven_digits_1.write_output("3")
    while not GPIO.input(STOP_BUTTON):
        for j in range(0, 8):
            print(j)
            seven_digits_2.write_output( pow(2,j) )
            time.sleep(0.2)

    time.sleep(2)

    # step 4
    seven_digits_1.set_light_off("dc")
    seven_digits_2.set_light_off("dc")
    seven_digits_1.write_output("4")

    while not GPIO.input(STOP_BUTTON):
        for j in range(1,7):
            f = 1 << j
            print(f)
            seven_digits_2.write_output(f)
            time.sleep(0.2)

    time.sleep(5)

    # clean the GPIO
    GPIO.cleanup()

def main2():

    #init electronic components
    init_electronic()

    eight_outputs = SN74HC595( (23, 24, 25, 12, 20) )
    seven_digits = SevenDigits( (19, 26, 22, 27, 18, 13, 6, 17) )
    seven_digits_2 = SevenDigits(output_ports = None, use_direct_gpio = False, component_interface = eight_outputs)

    eight_outputs.allow_output(True)
    seven_digits.write_output("-")
    
    for j in range(0, 10):
        print(j)
        seven_digits_2.write_output(str(j))
        time.sleep(2)

    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    
