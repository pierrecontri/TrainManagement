#!/usr/bin/env python

class EightIODigits(object):

    class BIT:
        ON = True
        OFF = False
    
    eight_digits_keys = [chr(i) for i in range(97,104)]

    val_matrix = {
        "a": [1,0,0,0,0,0,0,0],
        "b": [0,1,0,0,0,0,0,0],
        "c": [0,0,1,0,0,0,0,0],
        "d": [0,0,0,1,0,0,0,0],
        "e": [0,0,0,0,1,0,0,0],
        "f": [0,0,0,0,0,1,0,0],
        "g": [0,0,0,0,0,0,1,0],
        "h": [0,0,0,0,0,0,0,1],
        " ": [0,0,0,0,0,0,0,0]
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

    def __init__(self, component_interface = None, bit_not_on = True, digits_rangs = 0):
        self.component_interface = component_interface
        self.bit_not_on = bit_not_on
        self.internal_matrix = SevenDigits.val_matrix
        self.value = 0
        self.shifts = 8 * digits_rangs

    def write_output(self, val) -> int:

        value_type = type(val)

        if value_type is int:
            self.value = self.get_output_int( val )

        elif value_type is list:
            self.value = self.get_output_byte_array( val )

        elif value_type is str:
            if len(val) > 1:
                val = val[0]
            
            bits_state = self.internal_matrix[val] if val in self.internal_matrix.keys() else self.internal_matrix[" "]
            self.value = self.get_output_byte_array( bits_state )

        calc_value = self.value << self.shifts
        
        if self.component_interface is not None:
            # write output on component interface
            # clean up the part of bytes
            reseted_octet_shifts = (self.component_interface.hold_value | (255 << self.shifts)) ^ (255 << self.shifts)
            self.component_interface.write_output( reseted_octet_shifts | calc_value )

        return calc_value

    def get_output_byte_array(self, bits_state) -> int:
        output_calc = EightIODigits.get_int_from_byte_array(bits_state)
        # output inverted 1 => 0 retract the result the one byte
        output_value = 255 ^ output_calc if self.bit_not_on else output_calc
        return output_value

    def get_output_int(self, value) -> int:
        return (255 ^ value if self.led_not_on else value)

    def clean(self, clean_dc = False) -> int:
        self.write_output(" ")
        if clean_dc:
            self.set_point_off()
        return 0

def main():
    print("Test EightIODigits")
    eight_io_digits = EightIODigits(component_interface = None, led_not_on = False, use_car_matrix = True, digits_rangs = 0)
    print(eight_io_digits.write_output(24))
    eight_io_digits.set_point_on()
    print(eight_io_digits.write_output(24))
    eight_io_digits.set_point_off()
    print(eight_io_digits.write_output(24))

    eight_io_digits = EightIODigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0)
    print(eight_io_digits.write_output(24))
    eight_io_digits.set_point_on()
    print(eight_io_digits.write_output(24))
    eight_io_digits.set_point_off()
    print(eight_io_digits.write_output(24))

    eight_io_digits = EightIODigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 0)
    print(eight_io_digits.write_output("a"))
    eight_io_digits.set_point_on()
    print(eight_io_digits.write_output("a"))
    eight_io_digits.set_point_off()
    print(eight_io_digits.write_output("a"))

    eight_io_digits = EightIODigits(component_interface = None, led_not_on = True, use_car_matrix = True, digits_rangs = 1)
    print(eight_io_digits.write_output("2"))
    eight_io_digits.set_point_on()
    print(eight_io_digits.write_output("2"))
    eight_io_digits.set_point_off()
    print(eight_io_digits.write_output("2"))


if __name__ == '__main__':
    main()
