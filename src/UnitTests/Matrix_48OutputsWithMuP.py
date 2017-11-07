#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("../ElectronicComponents"))
sys.path.append(os.path.realpath("../ElectronicModel"))
import random

import time ## Import 'time' library. Allows us to use 'sleep'
from ElectronicComponents import *
from ElectronicModel import *

# port for stop button
STOP_BUTTON = 21

def main():
    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    shiftreg_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17}, 48 )
    seven_digits_1 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 5 )
    seven_digits_2 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 4 )
    seven_digits_3 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 3 )
    seven_digits_4 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 2 )

    seven_digits_5 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_6 = SevenDigits( component_interface = shiftreg_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )

    shiftreg_outputs.allow_output(True)
    blinking_point = False

    itxmp = 0
    while not stop_button.stop_state:
        tmp_struct_time = time.localtime()
        str_hour = ("0" if tmp_struct_time.tm_hour < 10 else "") + str(tmp_struct_time.tm_hour)
        str_min  = ("0" if tmp_struct_time.tm_min  < 10 else "") + str(tmp_struct_time.tm_min)
        #print("%s: %s %s : %s %s" % (str(tmp_struct_time), str_min[0], str_min[1], str_hour[0], str_hour[1]))
        seven_digits_1.write_output( str_min[0] )
        seven_digits_2.write_output( str_min[1] )
        seven_digits_3.write_output( str_hour[0] )
        seven_digits_4.write_output( str_hour[1] + ("." if blinking_point else " ") )
        blinking_point = not(blinking_point)
        #seven_digits_5.write_output( str( random.randrange(0, 9) ) + ("." if random.randrange(0,5) == 0 else "") )
        #seven_digits_6.write_output( str( random.randrange(0, 9) ) + ("." if random.randrange(0,5) == 0 else ""))
        time.sleep(0.4)
        shiftreg_outputs.write_output( (shiftreg_outputs.hold_value & 0xffffffffff00) | (itxmp % 0xff) )
        itxmp = itxmp + 1
        #time.sleep(0.3)
    
    seven_digits_1.write_output("  ")
    seven_digits_2.write_output("  ")
    seven_digits_3.write_output("  ")
    seven_digits_4.write_output("  ")
    shiftreg_outputs.write_output( shiftreg_outputs.hold_value & 0xffffffffff00 )
    time.sleep(1)

    # clean the GPIO
    InitGPIO.clean()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        InitGPIO.clean()
    
