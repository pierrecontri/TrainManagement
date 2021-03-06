#!/usr/bin/env python

class SevenDigits:

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

    def __init__(self, component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0):
        self.component_interface = component_interface
        self.led_not_on = led_not_on
        self.internal_matrix = SevenDigits.car_matrix if use_car_matrix else SevenDigits.val_matrix
        self.value = 0
        self.point = False
        self.shifts = 8 * digits_rangs

    def write_output(self, val) -> int:

        value_type = type(val)

        if value_type is int:
            self.value = self.get_output_int( val )

        elif value_type is list:
            self.value = self.get_output_byte_array( val )

        elif value_type is str:
            if len(val) > 1:
                self.set_point_on(no_output = True) if "." == val[1] else self.set_point_off(no_output = True)
                val = val[0]
            
            leds_state = self.internal_matrix[val] if val in self.internal_matrix.keys() else self.internal_matrix[" "]
            self.value = self.get_output_byte_array( leds_state )

        point_value = (not int(self.point) if self.led_not_on else int(self.point) ) << 7
        calc_value = (self.value | point_value) << self.shifts
        
        if self.component_interface is not None:
            # write output on component interface
            # clean up the part of bytes
            reseted_octet_shifts = (self.component_interface.hold_value | (255 << self.shifts)) ^ (255 << self.shifts)
            self.component_interface.write_output( reseted_octet_shifts | calc_value )

        return calc_value

    def get_output_byte_array(self, leds_state) -> int:
        output_calc = SevenDigits.get_int_from_byte_array(leds_state)
        # output inverted 1 => 0 retract the result the one byte
        output_value = 127 ^ output_calc if self.led_not_on else output_calc
        return output_value

    def get_output_int(self, value) -> int:
        return (127 ^ value if self.led_not_on else value)

    def set_point_on(self, no_output = False) -> int:
        self.point = True
        return 0 if no_output else self.write_output(self.value)

    def set_point_off(self, no_output = False) -> int:
        self.point = False
        return 0 if no_output else self.write_output(self.value)

    def clean(self, clean_dc = False) -> int:
        self.write_output(" ")
        if clean_dc:
            self.set_point_off()
        return 0

def main():
    print("Test SevenDigits")
    seven_digits = SevenDigits(component_interface = None, led_not_on = False, use_car_matrix = True, digits_rangs = 0)
    print(seven_digits.write_output(24))
    seven_digits.set_point_on()
    print(seven_digits.write_output(24))
    seven_digits.set_point_off()
    print(seven_digits.write_output(24))

    seven_digits = SevenDigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0)
    print(seven_digits.write_output(24))
    seven_digits.set_point_on()
    print(seven_digits.write_output(24))
    seven_digits.set_point_off()
    print(seven_digits.write_output(24))

    seven_digits = SevenDigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0)
    print(seven_digits.write_output("a"))
    seven_digits.set_point_on()
    print(seven_digits.write_output("a"))
    seven_digits.set_point_off()
    print(seven_digits.write_output("a"))

    seven_digits = SevenDigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 1)
    print(seven_digits.write_output("2"))
    seven_digits.set_point_on()
    print(seven_digits.write_output("2"))
    seven_digits.set_point_off()
    print(seven_digits.write_output("2"))


if __name__ == '__main__':
    main()
