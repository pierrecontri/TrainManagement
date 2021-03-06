"""
It is an abstract module used like a library.
It is used to communicate between the TrainManagement server and the automate.
"""

# ---------------- Add Path  --------------------------------------------------
import sys
from sys import path as sys_pth
import os.path as pth

local_directory = pth.dirname(pth.abspath(__file__))
import_list = (
        pth.realpath(pth.join(local_directory, ".."))
        , pth.realpath(pth.join(local_directory, "..", "Model"))
)

for to_import in import_list:
  abs_pth = pth.abspath(to_import)
  if not pth.exists(abs_pth): continue
  if not abs_pth in sys_pth: sys_pth.append(abs_pth)
# -----------------------------------------------------------------------------

# TrainManagementController

import inspect
import abc

from Model import SwitchCommand
from ElectronicModel import EightIO

import threading
from time import sleep

class TrainManagementController(metaclass=abc.ABCMeta):
  """
Main Abstract Class for Train Management Controller
  """

  def __init__(self):
    """Constructor: preset the switchs list, command_switch_list and switchs_calue"""
    self._switchs_list = dict()
    self._command_switchs_list = list()
    self._switchs_value = 0
    for i in range(0, self.number_of_switchs_blocks):
      self._command_switchs_list.append( EightIO( component_interface = None, bit_not_on = False, digits_rangs = i ) )

  def contains_function(self, function_name: str):
    """Check if the function name input is contains into the controller (due to factory with external controller)"""
    return function_name in dir(self) and type(self.__getattribute__(function_name)).__name__ == 'method'

  def get_help(self):
    """This controller give some basics functions"""
    fct_lst = [fct for fct in dir(self) if type(self.__getattribute__(fct)).__name__ == 'method']
    concat_name_function = "\n".join([("- " + fl) for fl in fct_lst])

    return { 'help': "This controller give some basics functions:\n%s" % concat_name_function }

  def do(self, what, params: dict = {}):
    """From json request, get the action and execute it with parameters"""
    if not self.contains_function(what):
      return {'result': 'NOK', 'errorMessage': "The \"%s\" function does not exists!" % what}

    fct_do = self.__getattribute__(what)
    return fct_do(params) if len(inspect.getfullargspec(fct_do).args) > 1 else fct_do()

  def register_switch_value(self, switch_obj: SwitchCommand):
    """
    From a switch object, save it into a switch dictionary for matching with GUI
    """
    self._switchs_list[switch_obj.name] = switch_obj
    return

  def switch_value(self, switch_params: dict = {}):
    """
    From a json command with the switch name, find the switch object and inverse his value
    """
    sw_object = SwitchCommand.switch_from_json(switch_params)
    print("switchName: %s" % sw_object.name)

    switch_params["result"] = "NOK"

    if not sw_object.name in self._switchs_list.keys():
      self.bind_switch(switch_params)

    else:

      # get all connectors in the same group and put it to OFF
      tmp_switch_list = [tmp_switch
                         for tmp_switch in self._switchs_list.values()
                         if tmp_switch.group == self._switchs_list[sw_object.name].group
                            and tmp_switch.name != sw_object.name]

      for t_switch in tmp_switch_list:
        t_switch.state = SwitchCommand.OFF
        if not(t_switch.is_press):
          self.set_switch_value( t_switch.switch_to_json() )

      # set to ON the switch value
      self._switchs_list[sw_object.name].switch_value()

      # call the electronic part
      self.set_switch_value(sw_object.switch_to_json())
      switch_params["result"] = "OK"

    return switch_params

  def bind_switch(self, switch_params: dict):
    """
    From a json command (sent by GUI) bind a switch between is unique id name and his memory object
    """
    switch_object = SwitchCommand.switch_from_json(switch_params)
    #save the new switch object to the internal switches list
    self._switchs_list[switch_object.name] = switch_object

    switch_obj_return = SwitchCommand.switch_to_json(switch_object)
    switch_obj_return["result"] = "OK"

    return switch_obj_return

  def get_switch(self, switch_name: str, is_press: bool = True) -> SwitchCommand:
    """
    From the unique id name switch find it into the switch dictionary and return it
    If not exists, create a new entry in the dictionary
    """
    if not switch_name in self._switchs_list.keys():
      self.bind_switch( { 'switchName': switch_name, 'switchValue': '0', 'isPersistent': not(is_press) } )

    return self._switchs_list[switch_name]

  def get_switch_value(self, params: dict) -> dict:
    """
    Return the switch value
    """
    params["switchValue"] = self.get_switch(params["switchName"], not(params["isPersistent"] if "isPersistent" in params.keys() else False)).state
    params["result"] = "OK"
    get_value_txt = "get_switch_value : sw name '%(switchName)s', sw value '%(switchValue)d', result '%(result)s'" % params
    # use the driver to get the real switch value
    self.get_switch_value_handle ( get_value_txt )
    return params
  
  def set_switch_value(self, params: dict) -> dict:
    """
    Set the switch to other value
    Send order to the electronic component
    """
    if not "switchName" in params:
      raise Exception("fct: set_switch_value; no switchName available into params")

    sw_obj = self.get_switch(params["switchName"])
    print( "set_switch_value : sw name '%s', sw value '%s'" % (sw_obj.name, str(sw_obj.state)) )

    sw_id = int(sw_obj.name.split("_").pop())
    block_switch_number = int(sw_id / 8)

    params["result"] = "NOK"

    # internal function for bit calcultation
    def write_output(switch_number, value):
      val_ret = self._command_switchs_list[block_switch_number].write_output( value )

      switch_mask_blocks = pow(2, 8 * self.number_of_switchs_blocks) - 1
      switch_mask = switch_mask_blocks ^ pow(2, switch_number)
      self._switchs_value = (self._switchs_value & switch_mask ) | val_ret
      self.set_switch_value_handle ( self._switchs_value )

    val_to_send = sw_obj.state << (sw_id % 8)

    if sw_id >= (len(self._command_switchs_list) * 8):
      params["result"] = "NOK"
      params["errorMessage"] = "no more switch block instanciate into controller"
      raise Exception("Error: %s" % params["errorMessage"])

    write_output( sw_id, val_to_send )
    print("on press:    %d" % self._switchs_value)

    if sw_obj.is_press:
      sleep(0.15)

      write_output( sw_id, SwitchCommand.OFF )
      print("after press: %d" % self._switchs_value)

    params["result"] = "OK"

    return params

  def emergency_stop(self) -> dict:
    """
    Emmergency function: send a broadcast message to all electronic controllers
    """
    for cs in self._command_switchs_list:
      cs.write_output( SwitchCommand.OFF )

    self._switchs_value = 0
    self.set_switch_value_handle ( self._switchs_value )

    return {'emergency_stop': 'done'}

  def async_send_message(self, async_message):
    """
    Due to Python 2 migration, the oldest way to call a async method
    """
    t_msg = threading.Thread( target=self.send_message, args=(async_message,) )
    t_msg.daemon = False
    t_msg.start()
    sleep(0.8)
    return

  # Abstract methods
  # Force the end user to code his real electronic comportment

  @abc.abstractmethod
  def start_demo(self):
    pass

  @abc.abstractmethod
  def stop_demo(self):
    pass

  @abc.abstractmethod
  def get_status(self):
    pass

  @abc.abstractmethod
  def send_message(self, message):
    pass

  @abc.abstractmethod
  def get_switch_value_handle(self, params):
    pass

  @abc.abstractmethod
  def set_switch_value_handle(self, params):
    pass

  @abc.abstractproperty
  def number_of_switchs_blocks(self):
    """ Define the cascade components for 8 bits serial """
    pass

  def get_light_info(self):
    pass

  def set_light(self):
    pass

  def get_direction_info(self):
    pass

  def set_direction(self):
    pass


# Unit Tests
if __name__ == '__main__':
  # due to the abstractmethod, the tests is deported on DummyController
  # I'm so stupid guy, I can make test even if it is abstract !

  class TestController(TrainManagementController):

    def __init__(self):
      self._number_of_switchs_blocks = 3
      TrainManagementController.__init__(self)

    @property
    def number_of_switchs_blocks(self):
      """ Define the cascade components for 8 bits serial """
      return self._number_of_switchs_blocks

    def start_demo(self):
      return { "Start demo": "OK" }

    def stop_demo(self):
      return { "Stop demo": "OK" }

    def get_status(self):
      return { 'get_status': 'OK' }
    
    def get_switch_value_handle(self, params):
      return { 'get_switch_value': 'OK' }
    
    def set_switch_value_handle(self, params):
      return { 'set_switch_value': 'OK' }
    
    def get_light_info(self):
      return { 'get_light_info': 'OK' }
    
    def set_light(self):
      return { 'set_light': 'OK' }
    
    def get_direction_info(self):
      return { 'get_direction_info': 'OK' }
    
    def set_direction(self):
      return { 'set_direction': 'OK' }

    def send_message(self, msg):
      print("Message sent: %s" % msg)

  test_controller = TestController()
  test_controller.register_switch_value(SwitchCommand("sw1_0", "grp1"))
  test_controller.register_switch_value(SwitchCommand("sw1_1", "grp1"))
  test_controller.register_switch_value(SwitchCommand("sw2_2", "grp2", False))
  test_controller.register_switch_value(SwitchCommand("sw2_3", "grp2", False))

  test_controller.register_switch_value(SwitchCommand("sw3_4", "grp3"))

  print( test_controller.get_help()['help'] )

  print( test_controller.do("start_demo", {}) )
  print( test_controller.do("stop_demo", {}) )
  print( test_controller.do("get_status", {}) )
  print( test_controller.do("get_switch_value", {"switchName":"sw1_0"}) )
  print( test_controller.do("get_switch_value", {"switchName":"sw1_1"}) )
  print( test_controller.do("set_switch_value", {"switchName":"sw1_0"}) )
  print( test_controller.do("set_switch_value", {"switchName":"sw1_1"}) )
  print( test_controller.do("get_light_info", {}) )
  print( test_controller.do("set_light", {}) )
  print( test_controller.do("get_direction_info", {}) )
  print( test_controller.do("set_direction", {}) )

  print("sw1_0: %s" % test_controller.do("get_switch_value", {"switchName":"sw1_0"}))
  print("sw1_0: %s" % test_controller.get_switch("sw1_0").state )
  test_controller.do("switch_value", {"switchName":"sw1_0", "switchValue":1} )
  print("sw1_0: %s" %  test_controller.get_switch("sw1_0").state )
  print("sw1_1: %s\n" %  test_controller.get_switch("sw1_1").state )

  print("sw1_0: %s" % test_controller.do("get_switch_value", {"switchName":"sw1_1"}))
  print("sw1_1: %s" % test_controller.get_switch("sw1_1").state )
  test_controller.do("switch_value", {"switchName":"sw1_1", "switchValue":1} )
  print("sw1_0: %s" %  test_controller.get_switch("sw1_0").state )
  print("sw1_1: %s" %  test_controller.get_switch("sw1_1").state )

  pass
