#!/usr/bin/env python

# ---------------------------------------------------------------------
# ------------------- INCLUDING MANAGEMENT ----------------------------
from sys import path as sys_pth
import os.path as pth

local_directory = pth.dirname(pth.abspath(__file__))
import_list = [local_directory
               # , pth.join(local_directory, "..","ElectronicComponents")
               # , pth.join(local_directory, "..","ElectronicModel")
]

for to_import in import_list:
  abs_dir = pth.dirname(pth.abspath(to_import))
  if not abs_dir in sys_pth: sys_pth.append(abs_dir)
# ---------------------------------------------------------------------

import time
from ElectronicComponents import *

class SwitchsCommand(object):
    """
SwitchCommands: this class make the interface between the logical demand
and the electronical interface
    """
    def __init__(self, train_direction):
        self.train_direction = train_direction
    
    def change_switch(self, device):
        """
Function change_switch
input  : device as int -> constant value from TrainDirection
output : none
        """
        old_value = self.train_direction.get_value(device)
        self.train_direction.set_value(device, not(old_value))
        if not (self.train_direction.is_on_off_switch(device)):
            time.sleep(0.2)
            self.train_direction.set_value(device, False)

def unit_tests():
    import TrainDirection as td
    InitGPIO.init_electronic()
    sc = SwitchsCommand(td.TrainDirection)
    sc.change_switch(td.TrainDirection.PARK2_TURN)

if __name__ == '__main__':
    unit_tests()
