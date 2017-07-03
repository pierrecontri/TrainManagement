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
  pass