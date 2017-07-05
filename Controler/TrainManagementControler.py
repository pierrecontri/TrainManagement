# TrainManagementControler

import inspect
import abc

class TrainManagementControler(metaclass=abc.ABCMeta):
  """
Main Abstract Class for Train Management Controler
  """

  def __init__(self):
    pass

  def contains_function(self, function_name):
    return function_name in dir(self) and type(self.__getattribute__(function_name)).__name__ == 'method'

  def get_help(self):
    fct_lst = [fct for fct in dir(self) if type(self.__getattribute__(fct)).__name__ == 'method']
    concat_name_function = "\n".join([("- " + fl) for fl in fct_lst])

    return { 'help': "This controler give some basics functions:\n%s" % concat_name_function }

  def do(self, what, params = {}):

    if not self.contains_function(what):
      return {'error': "The \"%s\" function does not exists!" % what}

    fct_do = self.__getattribute__(what)
    args_specs = inspect.getargspec(fct_do)

    return fct_do(params) if len(args_specs.args) > 1 else fct_do()

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
  def get_switch_info(self, params):
    pass

  @abc.abstractmethod
  def set_switch_value(self, params):
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
    
      def get_switch_info(self, params):
        return { 'get_switch_info': 'OK' }
    
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

  print( test_controler.get_help()['help'] )

  print( test_controler.do("start_demo", {}) )
  print( test_controler.do("stop_demo", {}) )
  print( test_controler.do("get_status", {}) )
  print( test_controler.do("get_switch_info", {}) )
  print( test_controler.do("set_switch_value", {}) )
  print( test_controler.do("get_light_info", {}) )
  print( test_controler.do("set_light", {}) )
  print( test_controler.do("get_direction_info", {}) )
  print( test_controler.do("set_direction", {}) )

  pass