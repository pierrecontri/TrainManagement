# TrainManagementControler

import threading, time
import inspect

class Controler(object):

  # functions_list = ['get_help', 'get_status', 'get_switch_info', 'set_switch', 'set_light', 'set_direction']

  def contains_function(self, function_name):
    return function_name in Controler.__dict__.keys() and type(Controler.__dict__[function_name]).__name__ == 'function'

  def get_help(self):
    #concat_name_function = "\n".join([("- " + fl) for fl in Controler.functions_list])
    fct_lst = [fct for fct in Controler.__dict__.keys() if type(Controler.__dict__[fct]).__name__ == 'function']
    concat_name_function = "\n".join([("- " + fl) for fl in fct_lst])
    str_return = "This controler give some basics functions:\n%s" % concat_name_function
    return { 'help': str_return }

  def start_demo(self):

    from sys import path as sys_pth
    import os.path as pth

    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory, "..","UnitTests")
                        #, pth.join(local_directory, "..","ElectronicComponents")
                        ,# pth.join(local_directory, "..","ElectronicModel")
    ]

    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)

    from UnitTests import Time_32OutputsWithMuP as  t32
    from UnitTests import ChaseWithMuP as cwmp

    t_time = threading.Thread( target=t32.time_32outputs, args=() )
    t_chase = threading.Thread( target=cwmp.chase_demo, args=() )

    t_time.daemon = True
    t_chase.daemon = True

    t_time.start()
    t_chase.start()

    time.sleep(20)

    return {'start_demo': 'done'}

  def get_status(self):
    return { 'Status': 'System OK' }

  def get_switch_info(self, params):
    params["result"] = "OK"
    return

  def set_switch_value(self, params):
    # add the controler code here
    self.get_switch_info(params)
    return params

  def get_light_info(self):
    pass

  def set_light(self):
    pass

  def get_direction_info(self):
    pass

  def set_direction(self):
    pass

  def do(self, what, params = {}):

    fct_do = Controler.__dict__[what] #if self.contains_function(what) else ""
    args_specs = inspect.getargspec(fct_do)

    return fct_do(self, params) if  "params" in args_specs.args else fct_do(self)


# Unit Tests
if __name__ == '__main__':
  # relative import path

  ctrl = Controler()
  ctrl.start_demo()
