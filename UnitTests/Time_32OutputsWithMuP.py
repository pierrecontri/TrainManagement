#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.realpath("ElectronicComponents"))
sys.path.append(os.path.realpath("ElectronicModel"))

import time ## Import 'time' library. Allows us to use 'sleep'
import queue
from ElectronicComponents import *
from ElectronicModel import *

# port for stop button
STOP_BUTTON = 21

def time_32outputs( master_thread_queue = None ):

    t_queue = None

    # manage the thread queue if not null
    if master_thread_queue is not None:
        t_queue = queue.Queue()
        master_thread_queue.append(t_queue)

    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    sixteen_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17}, 32 )
    seven_digits_1 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 3 )
    seven_digits_2 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 2 )
    seven_digits_3 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_4 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )

    print("Time  ON")

    sixteen_outputs.allow_output(True)
    blinking_point = False

    do_stop = False

    while not stop_button.stop_state and not do_stop:
        tmp_struct_time = time.localtime()
        str_hour = ("0" if tmp_struct_time.tm_hour < 10 else "") + str(tmp_struct_time.tm_hour)
        str_min  = ("0" if tmp_struct_time.tm_min  < 10 else "") + str(tmp_struct_time.tm_min)
        #print("%s: %s %s : %s %s" % (str(tmp_struct_time), str_min[0], str_min[1], str_hour[0], str_hour[1]))
        seven_digits_1.write_output( str_min[0] )
        seven_digits_2.write_output( str_min[1] )
        seven_digits_3.write_output( str_hour[0] )
        seven_digits_4.write_output( str_hour[1] + ("." if blinking_point else " ") )
        blinking_point = not(blinking_point)
        time.sleep(0.4)
        # thread management if exists
        if t_queue is not None and t_queue.qsize() > 0:
            msg = t_queue.get(False)
            if msg == "stop": do_stop = True
    
    seven_digits_1.write_output("  ")
    seven_digits_2.write_output("  ")
    seven_digits_3.write_output("  ")
    seven_digits_4.write_output("  ")

    # clean the GPIO
    InitGPIO.clean()

    print("Time  OFF")


if __name__ == '__main__':
    try:
        time_32outputs()
    except KeyboardInterrupt:
        InitGPIO.clean()
    
