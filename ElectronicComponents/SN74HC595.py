#!/usr/bin/env python3

import RPi.GPIO as GPIO ## Import GPIO library

class SN74HC595(object):

    def __init__(self, inputs_ports, outputs_len = 8):
        if type(inputs_ports) is not dict or len(inputs_ports) != 5:
            raise ValueError('Inputs_ports need 5 entries ports number in dict')

        self.outputs_len = outputs_len
        self.rclk, self.srclr, self.srclk, self.ser, self.oe = \
                   (inputs_ports['rclk'],inputs_ports['srclr'],inputs_ports['srclk'],inputs_ports['ser'],inputs_ports['oe'])
        self.value = 0

        GPIO.setwarnings(False)
        for val in self.inputs.values():
            GPIO.setup(val, GPIO.OUT)

        self.allow_output(False)
        GPIO.output(self.srclr, True)

    def allow_output(self, val):
        if self.oe is not None:
            GPIO.output(self.oe, not(bool(val)))
    
    def write_output(self, octet):

        self.value = octet

        GPIO.output(self.rclk, False)

        for i in range(0, self.outputs_len):
            GPIO.output(self.srclk, False)
            val_state = bool(octet & 1)
            GPIO.output(self.ser, val_state)
            GPIO.output(self.srclk, True)
            octet = octet >> 1

        GPIO.output(self.rclk, True)

    @property
    def inputs(self) -> dict:
        return {'rclk':self.rclk, 'srclr':self.srclr, 'srclk':self.srclk, 'ser':self.ser, 'oe':self.oe}

    @property
    def hold_value(self) -> int:
        return self.value

if __name__ == '__main__':
    import time
    GPIO.setmode(GPIO.BCM)
    eight_outputs = SN74HC595({'ser':5, 'oe':6, 'rclk':13, 'srclk':19, 'srclr':26})

    tmpInputs = eight_outputs.inputs
    print("  " + "_" * 15)
    print(" | %s | %s |" % ("Input", "Value"))
    print(" |" + "_" * 15 + "|")
    for k in tmpInputs:
        print(" | %5s | %5s |" % (k, tmpInputs[k]))
    print(" |" + "_" * 15 + "|")
        
    eight_outputs.allow_output(True)
    for i in range(0, 8):
        eight_outputs.write_output(1 << i)
        time.sleep(0.5)
    eight_outputs.write_output(255)
    time.sleep(2)
    GPIO.cleanup()
