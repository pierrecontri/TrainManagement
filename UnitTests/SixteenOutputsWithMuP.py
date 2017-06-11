#!/usr/bin/env python

import sys, os
sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("../ElectronicComponents"))
sys.path.append(os.path.realpath("../ElectronicModel"))

import time ## Import 'time' library. Allows us to use 'sleep'
from ElectronicComponents import *
from ElectronicModel import *

# port for stop button
STOP_BUTTON = 21

def main7():
    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    sixteen_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17}, 16 )
    seven_digits_1 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_2 = SevenDigits( component_interface = sixteen_outputs, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )

    sixteen_outputs.allow_output(True)

    for i in range(99, -1, -1):
        seven_digits_1.write_output(str(int(i / 10)))
        seven_digits_2.write_output(str(i % 10))
        time.sleep(0.05)
    
    seven_digits_1.write_output(" ")
    seven_digits_2.write_output(" ")
    time.sleep(1)

    # clean the GPIO
    InitGPIO.clean()

def main6():
    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    sixteen_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17}, 16 )
    seven_digits_1 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_2 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )

    sixteen_outputs.allow_output(True)

    for i in range(99, -1, -1):
        val1 = seven_digits_1.write_output(str(int(i / 10)))
        val2 = seven_digits_2.write_output(str(i % 10))
        print("%d\t%d" % (val1, val2))
        sixteen_outputs.write_output(val1 | val2)
        time.sleep(0.02)
    
    val1 = seven_digits_1.write_output(" ")
    val2 = seven_digits_2.write_output(" ")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(1)

    # clean the GPIO
    InitGPIO.clean()

def main5():

    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    sixteen_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17}, 16 )
    seven_digits_1 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_2 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )

    sixteen_outputs.allow_output(True)

    val1 = seven_digits_1.write_output("1")
    val2 = seven_digits_2.write_output("2")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    seven_digits_1.set_point_on()

    val1 = seven_digits_1.write_output("a")
    val2 = seven_digits_2.write_output("b")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    seven_digits_1.set_point_off()
    seven_digits_2.set_point_on()

    val1 = seven_digits_1.write_output("6")
    val2 = seven_digits_2.write_output("9")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    seven_digits_2.set_point_off()

    val1 = seven_digits_1.write_output("0")
    val2 = seven_digits_2.write_output("0")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    val1 = seven_digits_1.write_output(" ")
    val2 = seven_digits_2.write_output(" ")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    val1 = seven_digits_1.write_output("3.")
    val2 = seven_digits_2.write_output("4.")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    val1 = seven_digits_1.write_output("8")
    val2 = seven_digits_2.write_output("-")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    val1 = seven_digits_1.write_output("5 ")
    val2 = seven_digits_2.write_output("7 ")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    val1 = seven_digits_1.write_output(" ")
    val2 = seven_digits_2.write_output(" ")
    print("%d\t%d" % (val1, val2))
    sixteen_outputs.write_output(val1 | val2)
    time.sleep(2)

    # clean the GPIO
    InitGPIO.clean()


def main4():

    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    sixteen_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17} )
    chase = Chase(256)

    sixteen_outputs.allow_output(True)

    while not stop_button.stop_state:
        ti = chase.ticks()
        print(ti)
        sixteen_outputs.write_output( ti )
        time.sleep(0.2)

    sixteen_outputs.write_output( 256 )
    time.sleep(2)
    
    sixteen_outputs.write_output( 0 )
    time.sleep(2)

    sixteen_outputs.write_output( 128 )
    time.sleep(2)

    sixteen_outputs.write_output( 128 << 8 )
    time.sleep(2)
    
    sixteen_outputs.write_output( 0 )
    time.sleep(2)

    # clean the GPIO
    InitGPIO.clean()


def main3():

    #init electronic components
    InitGPIO.init_electronic()
    stop_button = StopButton(STOP_BUTTON)
    eight_outputs = SN74HC595( {'ser':24,'oe':23,'rclk':22,'srclk':27,'srclr':17} )
    seven_digits_1 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 1 )
    seven_digits_2 = SevenDigits( component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0 )
    chase = Chase(256)
    dummyChase = False

    eight_outputs.allow_output(True)

    i = 0

    # step 1
    val1 = seven_digits_1.set_point_on()
    val2 = seven_digits_2.set_point_off()
    eight_outputs.write_output(val1 | val2)
    
    while not stop_button.stop_state:
        output_mod1 = str(hex(i % 16))[-1]
        output_mod2 = str(hex(int((i / 16) % 16)))[-1]

        #seven_digits_1.write_output( output_mod1 )
        if dummyChase:
            eight_outputs.write_output( chase.ticks() )
        else:
            val2 = seven_digits_2.write_output( output_mod2 )
            eight_outputs.write_output(val1 | val2)

        i += 1
        time.sleep(0.2)

    time.sleep(2)

    # step 2
    val1 = seven_digits_1.set_point_off()
    val2 = seven_digits_2.set_point_on()
    val1 = seven_digits_1.write_output("2")
    eight_outputs.write_output(val1 | val2)
    while not stop_button.stop_state:
        for j in range(97, 103):
            val2 = seven_digits_2.write_output( chr(j) )
            eight_outputs.write_output(val1 | val2)
            time.sleep(0.2)

    time.sleep(2)

    # step 3
    val1 = seven_digits_1.set_point_on()
    val2 = seven_digits_2.set_point_on()
    val1 = seven_digits_1.write_output("3")
    eight_outputs.write_output(val1 | val2)
    while not stop_button.stop_state:
        for j in range(0, 8):
            print(j)
            val2 = seven_digits_2.write_output( pow(2,j) )
            eight_outputs.write_output(val1 | val2)
            time.sleep(0.2)

    time.sleep(2)

    # step 4
    val1 = seven_digits_1.set_point_off()
    val2 = seven_digits_2.set_point_off()
    val1 = seven_digits_1.write_output("4")
    eight_outputs.write_output(val1 | val2)
    while not stop_button.stop_state:
        for j in range(1,7):
            f = 1 << j
            print(f)
            val2 = seven_digits_2.write_output(f)
            eight_outputs.write_output(val1 | val2)
            time.sleep(0.2)

    time.sleep(5)

    eight_outputs.write_output(0)
    time.sleep(2)

    eight_outputs.write_output(127)
    time.sleep(2)

    eight_outputs.write_output(255)
    time.sleep(2)

    eight_outputs.write_output(127 << 8)
    time.sleep(2)

    eight_outputs.write_output(255 << 8)
    time.sleep(0.2)

    # clean the GPIO
    InitGPIO.clean()

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
        main7()
    except KeyboardInterrupt:
        InitGPIO.clean()
    
