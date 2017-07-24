if __name__ == "__main__":
  # ---------------- Add Path  --------------------------------------------------
  import sys
  from sys import path as sys_pth
  import os.path as pth
  
  local_directory = pth.dirname(pth.abspath(__file__))
  import_list = [local_directory
            , pth.join(local_directory,"../Controler")
            , pth.join(local_directory,"../Model")
  ]
  
  for to_import in import_list:
    abs_dir = pth.dirname(pth.abspath(to_import))
    if not abs_dir in sys_pth: sys_pth.append(abs_dir)
  # -----------------------------------------------------------------------------

from Model import SwitchCommand
from Controler.TrainManagementControler import TrainManagementControler
from ElectronicModel import EightIO
import random, time

class DummyElec(object):

  def __init__(self):
    self.value = 0

  def write_output(self, value):
    self.value = value
    print("DummyElec write_output: %s" % value)

  @property
  def hold_value(self) -> int:
    return self.value

class Controler(TrainManagementControler):

  def __init__(self):
    self._number_of_switchs_blocks = 4
    TrainManagementControler.__init__(self)
    dummy_elec = DummyElec()
    for t_cmd_switch in self._command_switchs_list:
      t_cmd_switch.component_interface = dummy_elec

  @property
  def number_of_switchs_blocks(self):
    return self._number_of_switchs_blocks

  def get_status(self):
    return { 'Status': 'System OK' }

  def start_demo(self):
    print("DummyDo")
    print((self.get_help())['help'])
    return {'start_demo': 'done'}

  def stop_demo(self):
    return {'stop_demo': 'done'}

  # def get_switch_value(self, params):
    # """
    # Return the switch value
    # """
    # params["switchValue"] = self.get_switch(params["switchName"]).state
    # params["result"] = "OK"
    # print( "get_switch_value : sw name '%(switchName)s', sw value '%(switchValue)s', result '%(result)s'" % params )

    # return params
  
  # def set_switch_value(self, params):
    # """
    # Set the switch to other value
    # Send order to the electronic component
    # """

    # switch_name, switch_value = (params["switchName"], params["switchValue"])
    # print( "set_switch_value : sw name '%s', sw value '%s'" % (switch_name, switch_value) )

    # tmp_switch = self.get_switch(params["switchName"])
    # sw_id = int(tmp_switch.name.split("_").pop())
    # block_switch_number = int(sw_id / 8)
    # tmp_switch_value = sw_id % 8

    # print("on press:    %s" % bin(self._command_switchs_list[block_switch_number].write_output( chr( 97 + tmp_switch_value ) )) )

    # if tmp_switch.is_press:
      # time.sleep(0.2)
      # print("after press: %s" % bin(self._command_switchs_list[block_switch_number].write_output( " " )) )

    # params["result"] = "OK"

    # return params

  def get_switch_value_handle(self, value):
    print(value)

  def set_switch_value_handle(self, value):
    print(value)

# units tests
if __name__ == "__main__":
  print("DummyControler")
  ctrl = Controler()

  print( dir(ctrl) )

  ctrl.register_switch_value(SwitchCommand("sw1_0", "sw1"))
  ctrl.register_switch_value(SwitchCommand("sw1_1", "sw1"))
  ctrl.register_switch_value(SwitchCommand("sw2_2", "sw2"))
  ctrl.register_switch_value(SwitchCommand("sw2_3", "sw2"))

  ctrl.register_switch_value(SwitchCommand(name = "sw3_0", group = "sw3", is_press = False))

  ctrl.do("get_help")
  from time import sleep
  print("Start Demo: %s" % ctrl.start_demo())
  # sleep(2)
  print("Stop Demo: %s" % ctrl.stop_demo())

  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  ctrl.switch_value( {"switchName":"sw1_0", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw1_1").state )
  
  print("s2: %s" % ctrl.get_switch("sw1_1").state )
  ctrl.switch_value( {"switchName":"sw1_1", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw1_1").state )
  
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  ctrl.switch_value( {"switchName":"sw2_2", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw2_3").state )
  
  print("s4: %s" % ctrl.get_switch("sw2_3").state )
  ctrl.switch_value( {"switchName":"sw2_3", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw2_3").state )



# using
# python -m ElectronicControler.DummyControler