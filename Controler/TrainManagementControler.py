if __name__ == "__main__":
    # ---------------- Add Path  --------------------------------------------------
    import sys
    from sys import path as sys_pth
    import os.path as pth
    
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory,"../Controler")
    ]
    
    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)
    # -----------------------------------------------------------------------------


# TrainManagementControler

import inspect
import abc

from Model import SwitchCommand
from ElectronicModel import EightIO

import time

class TrainManagementControler(metaclass=abc.ABCMeta):
  """
Main Abstract Class for Train Management Controler
  """

  def __init__(self):
    self._switchs_list = dict()
    self._command_switchs_list = list()
    for i in range(0, self.number_of_switchs_blocks):
      self._command_switchs_list.append( EightIO( component_interface = None, bit_not_on = False, digits_rangs = i ) )

  def contains_function(self, function_name):
    return function_name in dir(self) and type(self.__getattribute__(function_name)).__name__ == 'method'

  def get_help(self):
    fct_lst = [fct for fct in dir(self) if type(self.__getattribute__(fct)).__name__ == 'method']
    concat_name_function = "\n".join([("- " + fl) for fl in fct_lst])

    return { 'help': "This controler give some basics functions:\n%s" % concat_name_function }

  def do(self, what, params = {}):

    if not self.contains_function(what):
      return {'result': 'NOK', 'errorMessage': "The \"%s\" function does not exists!" % what}

    fct_do = self.__getattribute__(what)
    args_specs = inspect.getargspec(fct_do)

    return fct_do(params) if len(args_specs.args) > 1 else fct_do()

  def register_switch_value(self, switch_obj):
    self._switchs_list[switch_obj.name] = switch_obj
    return

  def switch_value(self, switch_params = {}):

    sw_object = SwitchCommand.switch_from_json(switch_params)
    print("switchName: %s" % sw_object.name)

    switch_params["result"] = "NOK"

    if not sw_object.name in self._switchs_list.keys(): self.bind_switch(switch_params)
    else:

      # get all connectors in the same group and put it to OFF
      tmp_switch_list = [tmp_switch for tmp_switch in self._switchs_list.values() if tmp_switch.group == self._switchs_list[sw_object.name].group and not tmp_switch.name == sw_object.name]
      for t_switch in tmp_switch_list:
        t_switch.state = SwitchCommand.OFF
      #  if not(t_switch.is_press):
      #    self.set_switch_value( {'switchName': t_switch.name, 'switchValue': t_switch.state, 'isPersistent': not(t_switch.is_press)} )
      #    time.sleep(0.3)

      # set to ON the switch value
      self._switchs_list[sw_object.name].state = SwitchCommand.ON

      # call the electronic part
      self.set_switch_value(switch_params)
      switch_params["result"] = "OK"

    return switch_params

  def bind_switch(self, switch_params):
    switch_object = SwitchCommand.switch_from_json(switch_params)
    #instanciate the switch command object
    self._switchs_list[switch_object.name] = switch_object

    switch_obj_return = SwitchCommand.switch_to_json(switch_object)
    switch_obj_return["result"] = "OK"

    return switch_obj_return

  def get_switch(self, switch_name, is_press = True):
    if not switch_name in self._switchs_list.keys(): self.bind_switch( { 'switchName': switch_name, 'switchValue': '0', 'isPersistent': not(is_press) } )

    return self._switchs_list[switch_name]

  def get_switch_value(self, params):
    """
    Return the switch value
    """
    params["switchValue"] = self.get_switch(params["switchName"], not(params["isPersistent"] if "isPersistent" in params.keys() else False)).state
    params["result"] = "OK"
    self.get_switch_value_handle ( "get_switch_value : sw name '%(switchName)s', sw value '%(switchValue)s', result '%(result)s'" % params )

    return params
  
  def set_switch_value(self, params):
    """
    Set the switch to other value
    Send order to the electronic component
    """

    switch_name, switch_value, switch_persist = (params["switchName"], params["switchValue"], params["isPersistent"] if "isPersistent" in params.keys() else False)
    print( "set_switch_value : sw name '%s', sw value '%s'" % (switch_name, switch_value) )

    tmp_switch = self.get_switch(params["switchName"], not(switch_persist))
    sw_id = int(tmp_switch.name.split("_").pop())
    block_switch_number = int(sw_id / 8)
    tmp_switch_value = sw_id % 8

    val_to_send = self._switchs_list[switch_name].state << tmp_switch_value

    if block_switch_number > len(self._command_switchs_list) - 1:
      params["result"] = "NOK"
      params["errorMessage"] = "no more switch block instanciate into controler"
      raise Exception("Error: %s" % params["errorMessage"])

    val_ret = self._command_switchs_list[block_switch_number].write_output( val_to_send )

    print("--> Value to send: %s" % val_ret)
    
    print("on press:    ")
    self.set_switch_value_handle ( val_ret )

    if tmp_switch.is_press:
      time.sleep(0.2)
      val_ret = self._command_switchs_list[block_switch_number].write_output( " " )

      print("after press: ")
      self.set_switch_value_handle ( val_ret )

    params["result"] = "OK"

    return params

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
  def get_switch_value_handle(self, params):
    pass

  @abc.abstractmethod
  def set_switch_value_handle(self, params):
    pass

  @abc.abstractproperty
  def number_of_switchs_blocks(self):
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
  # due to the abstractmethod, the tests is deported on DummyControler
  # I'm so stupid guy, I can make test even if it is abstract !

  class TestControler(TrainManagementControler):
      def start_demo(self):
        return { "Start demo": "OK" }

      def stop_demo(self):
        return { "Stop demo": "OK" }

      def get_status(self):
        return { 'get_status': 'OK' }
    
      def get_switch_value(self, params):
        return { 'get_switch_value': 'OK' }
    
      def set_switch_value(self, params):
        return { 'set_switch_value': 'OK' }
    
      def get_light_info(self):
        return { 'get_light_info': 'OK' }
    
      def set_light(self):
        return { 'set_light': 'OK' }
    
      def get_direction_info(self):
        return { 'get_direction_info': 'OK' }
    
      def set_direction(self):
        return { 'set_direction': 'OK' }


  test_controler = TestControler()
  test_controler.register_switch_value(SwitchCommand("sw1_0", "grp1"))
  test_controler.register_switch_value(SwitchCommand("sw1_1", "grp1"))

  print( test_controler.get_help()['help'] )

  print( test_controler.do("start_demo", {}) )
  print( test_controler.do("stop_demo", {}) )
  print( test_controler.do("get_status", {}) )
  print( test_controler.do("get_switch_value", {"switchName":"sw1_0"}) )
  print( test_controler.do("get_switch_value", {"switchName":"sw1_1"}) )
  print( test_controler.do("set_switch_value", {"switchName":"sw1_0","switchValue":1}) )
  print( test_controler.do("set_switch_value", {"switchName":"sw1_1","switchValue":1}) )
  print( test_controler.do("get_light_info", {}) )
  print( test_controler.do("set_light", {}) )
  print( test_controler.do("get_direction_info", {}) )
  print( test_controler.do("set_direction", {}) )

  print("sw1_0: %s" % test_controler.do("get_switch_value", {"switchName":"sw1_0"}))
  print("sw1_0: %s" % test_controler.get_switch("sw1_0").state )
  test_controler.do("switch_value", {"switchName":"sw1_0", "switchValue":1} )
  print("sw1_0: %s" %  test_controler.get_switch("sw1_0").state )
  print("sw1_1: %s\n" %  test_controler.get_switch("sw1_1").state )

  print("sw1_0: %s" % test_controler.do("get_switch_value", {"switchName":"sw1_1"}))
  print("sw1_1: %s" % test_controler.get_switch("sw1_1").state )
  test_controler.do("switch_value", {"switchName":"sw1_1", "switchValue":1} )
  print("sw1_0: %s" %  test_controler.get_switch("sw1_0").state )
  print("sw1_1: %s" %  test_controler.get_switch("sw1_1").state )

  pass
