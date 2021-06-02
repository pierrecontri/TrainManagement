"""
DummyController: simulator of the electronic controller. Used for Unit Tests and GUI developpement
"""

# ---------------- Add Path  --------------------------------------------------
import sys
from sys import path as sys_pth
import os.path as pth

local_directory = pth.dirname(pth.abspath(__file__))

import_list = (
          #local_directory
          pth.realpath(pth.join(local_directory, ".."))
          , pth.realpath(pth.join(local_directory, "..", "TrainLibraries.zip"))
          , pth.realpath(pth.join(local_directory, "..", "Controller"))
          , pth.realpath(pth.join(local_directory, "..", "Model"))
)

for to_import in import_list:
  if not pth.exists(to_import): continue
  if not to_import in sys_pth: sys_pth.append(to_import)
# -----------------------------------------------------------------------------


from Controller import TrainManagementController
import random
from time import sleep

class DummyElec(object):

  """ Simulate an electronic component for the dummy controller """

  def __init__(self):
    self.value = 0

  def write_output(self, value):
    self.value = value
    print("DummyElec write_output: %s" % value)

  @property
  def hold_value(self) -> int:
    return self.value

class Controller(TrainManagementController):

  """ This is the dummy Controller to simulate the real electronic communication """

  def __init__(self):
    self._number_of_switchs_blocks = 4
    TrainManagementController.__init__(self)
    dummy_elec = DummyElec()
    for t_cmd_switch in self._command_switchs_list:
      t_cmd_switch.component_interface = dummy_elec

  @property
  def number_of_switchs_blocks(self):
    """ Define the cascade components for 8 bits serial """
    return self._number_of_switchs_blocks

  def get_status(self):
    return { 'Status': 'System OK' }

  def start_demo(self):
    print("DummyDo")
    print((self.get_help())['help'])
    return {'start_demo': 'done'}

  def stop_demo(self):
    return {'stop_demo': 'done'}

  def send_message(self, message):
    print("MSG: %s" % message)
    return

  def get_switch_value_handle(self, value):
    print(value)

  def set_switch_value_handle(self, value):
    print("slow down")
    sleep(0.2)
    print(value)

# units tests
if __name__ == "__main__":

  from Model import SwitchCommand

  print("DummyController")
  ctrl = Controller()
  print( dir(ctrl) )

  ctrl.register_switch_value(SwitchCommand("sw0_0", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw0_1", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw1_2", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw1_3", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw2_4", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw2_5", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw3_6", "grp0"))
  ctrl.register_switch_value(SwitchCommand("sw3_7", "grp0"))

  ctrl.register_switch_value(SwitchCommand(name = "sw4_0", group = "grp1", is_press = False))
  ctrl.register_switch_value(SwitchCommand(name = "sw4_1", group = "grp1", is_press = False))
  ctrl.register_switch_value(SwitchCommand(name = "sw5_2", group = "grp2", is_press = False))
  ctrl.register_switch_value(SwitchCommand(name = "sw5_3", group = "grp2", is_press = False))

  ctrl.do("get_help")
  print("Start Demo: %s" % ctrl.start_demo())
  # sleep(2)
  print("Stop Demo: %s" % ctrl.stop_demo())

  print("s1: %s" % ctrl.get_switch("sw0_0").state )
  ctrl.switch_value( {"switchName":"sw0_0", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw0_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw0_1").state )
  
  print("s2: %s" % ctrl.get_switch("sw0_1").state )
  ctrl.switch_value( {"switchName":"sw0_1", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw0_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw0_1").state )
  
  print("s3: %s" % ctrl.get_switch("sw1_2").state )
  ctrl.switch_value( {"switchName":"sw1_2", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw1_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw1_3").state )
  
  print("s4: %s" % ctrl.get_switch("sw1_3").state )
  ctrl.switch_value( {"switchName":"sw1_3", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw1_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw1_3").state )

  # -- persistant switch
  print("s0: %s" % ctrl.get_switch("sw4_0").state )
  ctrl.switch_value( {"switchName":"sw4_0", "switchValue":1} )
  print("s0: %s" % ctrl.get_switch("sw4_0").state )
  print("s1: %s\n" % ctrl.get_switch("sw4_1").state )
  print("s2: %s" % ctrl.get_switch("sw5_2").state )
  print("s3: %s\n" % ctrl.get_switch("sw5_3").state )
  
  print("s3: %s" % ctrl.get_switch("sw5_3").state )
  ctrl.switch_value( {"switchName":"sw5_3", "switchValue":1} )
  print("s0: %s" % ctrl.get_switch("sw4_0").state )
  print("s1: %s\n" % ctrl.get_switch("sw4_1").state )
  print("s2: %s" % ctrl.get_switch("sw5_2").state )
  print("s3: %s\n" % ctrl.get_switch("sw5_3").state )

# using
# python -m ElectronicController.DummyController