#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.realpath(".."))

print('\n'.join(sys.path))
import time ## Import 'time' library. Allows us to use 'sleep'
import queue
from ElectronicComponents import InitGPIO, SN74HC595, StopButton
from ElectronicModel.Chase import Chase

# port for stop button
STOP_BUTTON = 21

def chase_demo( master_thread_queue = None ):

    t_queue = None

    # manage the thread queue if not null
    if master_thread_queue is not None:
        t_queue = queue.Queue()
        master_thread_queue.append(t_queue)

    #init electronic components
    InitGPIO.init_electronic()

    stop_button = StopButton(STOP_BUTTON)
    eight_outputs = SN74HC595( {'ser':5,'oe':6,'rclk':13,'srclk':19,'srclr':26} )
    chase = Chase()
    print("Chase ON")

    eight_outputs.allow_output(True)

    do_stop = False

    while not stop_button.stop_state and not do_stop:
        eight_outputs.write_output( chase.ticks() )
        time.sleep(0.05)
        # thread management if exists
        if t_queue is not None and t_queue.qsize() > 0:
            msg = t_queue.get(False)
            if msg == "stop": do_stop = True

    eight_outputs.write_output( 128 )

    # clean the GPIO
    InitGPIO.clean()
    print("Chase OFF")


if __name__ == '__main__':
    try:
        chase_demo()
    except KeyboardInterrupt:
        InitGPIO.clean()
    
