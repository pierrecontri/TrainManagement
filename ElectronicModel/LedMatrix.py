#!/usr/bin/env python

class LedMatrix:

    class LIGHT:
        ON = True
        OFF = False

    def __init__(self, rows, cols, component_interface = None, led_not_on = True, digits_rangs = 0):
        self.rows = rows
        self.cols = cols
        self.component_interface = component_interface
        self.led_not_on = led_not_on
        self.value = 0
        self.shifts = 16 * digits_rangs
