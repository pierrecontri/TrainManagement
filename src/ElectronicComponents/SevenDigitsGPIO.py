#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library

class SevenDigitsGPIO(object):

    class LIGHT:
        ON = True
        OFF = False
    
    seven_digits_keys = [chr(i) for i in range(97,103)]

    # dictionnary matix definition
    car_matrix = {
        "0": [1,1,1,1,1,1,0],
        "1": [0,1,1,0,0,0,0],
        "2": [1,1,0,1,1,0,1],
        "3": [1,1,1,1,0,0,1],
        "4": [0,1,1,0,0,1,1],
        "5": [1,0,1,1,0,1,1],
        "6": [1,0,1,1,1,1,1],
        "7": [1,1,1,0,0,0,0],
        "8": [1,1,1,1,1,1,1],
        "9": [1,1,1,1,0,1,1],
        "-": [0,0,0,0,0,0,1],
        "_": [0,0,0,1,0,0,0],
        "a": [1,1,1,0,1,1,1],
        "b": [0,0,1,1,1,1,1],
        "c": [1,0,0,1,1,1,0],
        "d": [0,1,1,1,1,0,1],
        "e": [1,0,0,1,1,1,1],
        "f": [1,0,0,0,1,1,1],
        " ": [0,0,0,0,0,0,0]
    }
    number_matrix_keys_sorted = [str(i) for i in range(0,10)]

    val_matrix = {
        "a": [1,0,0,0,0,0,0],
        "b": [0,1,0,0,0,0,0],
        "c": [0,0,1,0,0,0,0],
        "d": [0,0,0,1,0,0,0],
        "e": [0,0,0,0,1,0,0],
        "f": [0,0,0,0,0,1,0],
        "g": [0,0,0,0,0,0,1],
        " ": [0,0,0,0,0,0,0]
    }

    @staticmethod
    def get_int_from_byte_array(byte_array):
        join_byte = '0b' + ''.join([str(t) for t in byte_array])
        return int(join_byte, 2)

    @staticmethod
    def get_byte_array_from_int(val):
        v = [(1 if val & pow(2,v_x) else 0) for v_x in range(0,8)]
        v.reverse()
        return v

    def __init__(self, output_ports = None, use_direct_gpio = True, component_interface = None, led_not_on = True, use_car_matrix = True):
        self.output_ports = output_ports
        self.use_direct_gpio = use_direct_gpio
        self.component_interface = component_interface
        self.led_not_on = led_not_on
        self.internal_matrix = SevenDigits.car_matrix if use_car_matrix else SevenDigits.val_matrix
        
        if self.output_ports != None:

            if len(output_ports) != 8:
                raise ValueError('Outputs_ports need 8 entries ports number')

            self.seven_digits_matrix = {}
            self.seven_digits_matrix["a"] = output_ports[0]
            self.seven_digits_matrix["b"] = output_ports[1]
            self.seven_digits_matrix["c"] = output_ports[2]
            self.seven_digits_matrix["d"] = output_ports[3]
            self.seven_digits_matrix["e"] = output_ports[4]
            self.seven_digits_matrix["f"] = output_ports[5]
            self.seven_digits_matrix["g"] = output_ports[6]
            self.seven_digits_matrix["dc"] = output_ports[7]

            if use_direct_gpio: SevenDigits.init_gpio(self)

    def init_gpio(self):
        # init seven digits
        if self.use_direct_gpio:
            GPIO.setwarnings(False)
            for val in self.seven_digits_matrix.values():
                # switch off lights as initial
                GPIO.setup(val, GPIO.OUT, initial = self.led_not_on)
        elif self.component_interface != None:
            self.component_interface.clean(True)
            
    def write_output(self, val):

        value_type = type(val)

        if value_type is int:
            self.write_output_int( val )
            return

        if value_type is list:
            self.write_output_byte_array( val )
            return

        if value_type is str:
            leds_state = self.internal_matrix[val] if self.internal_matrix.has_key(val) else self.internal_matrix[" "]
            self.write_output_byte_array( leds_state )
            return

    def write_output_byte_array(self, leds_state):
        if self.use_direct_gpio:
            self.write_gpio_output(leds_state)
        else:
            output_calc = SevenDigits.get_int_from_byte_array(leds_state)
            # output inverted 1 => 0 retract the result the one byte
            output_value = 255 ^ output_calc if self.led_not_on else output_calc
            # write output
            self.component_interface.write_output(output_value)

    def write_output_int(self, value):
        if self.use_direct_gpio:
            self.write_gpio_output( SevenDigits.get_byte_array_from_int(value) )
        else:
            self.component_interface.write_output(255 ^ value if self.led_not_on else value)

    def write_gpio_output(self, byte_array):
        for i in range (0, 7):
            out_value = (SevenDigits.LIGHT.ON and byte_array[i]) ^ self.led_not_on
            GPIO.output( self.seven_digits_matrix[chr(i + 97)], out_value )

    def set_light_on(self, num):
        if self.use_direct_gpio:
            GPIO.output(self.seven_digits_matrix[num], SevenDigits.LIGHT.ON ^ self.led_not_on)
        else:
            pass

    def set_light_off(self, num):
        if self.use_direct_gpio:
            GPIO.output(self.seven_digits_matrix[num], SevenDigits.LIGHT.OFF ^ self.led_not_on)
        else:
            pass

    def clean(self, clean_dc = False):
        for i in range(97,103):
            GPIO.output(self.seven_digits_matrix[chr(i)], SevenDigits.LIGHT.OFF ^ self.led_not_on)
        if clean_dc:
            GPIO.output(self.seven_digits_matrix["dc"], SevenDigits.LIGHT.OFF ^ self.led_not_on)
