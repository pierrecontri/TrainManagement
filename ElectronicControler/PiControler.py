if __name__ == "__main__":
    # ---------------- Add Path  --------------------------------------------------
    import sys
    from sys import path as sys_pth
    import os.path as pth
    
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory,"../Controler")
#                        , pth.join(local_directory,"../ElectronicComponents")
#                        , pth.join(local_directory,"../ElectronicModel")
    ]
    
    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)
    # -----------------------------------------------------------------------------

import threading
from Controler.TrainManagementControler import TrainManagementControler

from ElectronicComponents import *
# from ElectronicModel import EightIO

import queue
import time

# thread queues list
thread_queues_demo = []

def broadcast_thread_event(data, queue_obj):
    for q in queue_obj:
        q.put(data)

class Controler(TrainManagementControler):
  """
PiControler the real controler to manage Raspberry Pi
  """

  def __init__(self):
    TrainManagementControler.__init__(self)
    InitGPIO.init_electronic()
    self._shift_register = SN74HC595( inputs_ports = {'ser':5,'oe':6,'rclk':13,'srclk':19,'srclr':26}, outputs_len = 8 * len( self._command_switchs_list ) )
    self._shift_register.allow_output(True)
    for t_cmd_switch in self._command_switchs_list: t_cmd_switch.component_interface = self._shift_register

  def get_status(self):
    return { 'Status': 'System OK' }

  def start_demo(self):

    from sys import path as sys_pth
    import os.path as pth

    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory, "..","UnitTests")
                        , pth.join(local_directory, "..","ElectronicComponents")
                        , pth.join(local_directory, "..","ElectronicModel")
    ]

    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)

    from UnitTests import Time_32OutputsWithMuP
    from UnitTests import ChaseWithMuP

    thread_queues_demo.clear()
    self.t_time = threading.Thread( target=Time_32OutputsWithMuP.time_32outputs, args=(thread_queues_demo,) )
    self.t_chase = threading.Thread( target=ChaseWithMuP.chase_demo, args=(thread_queues_demo,) )

    self.t_time.daemon = True
    self.t_chase.daemon = True

    self.t_time.start()
    self.t_chase.start()

    return {'start_demo': 'done'}

  def stop_demo(self):

    broadcast_thread_event("stop", thread_queues_demo)

    self.t_chase.join()
    self.t_time.join()

    return {'stop_demo': 'done'}

  # def get_switch_value(self, params):
    # params["switchValue"] = self.get_switch(params["switchName"]).state
    # params["result"] = "OK"

    # return params

  # def set_switch_value(self, params):
    # """
    # Set the switch to other value
    # Send order to the electronic component
    # """

    # tmp_switch = self.get_switch(params["switchName"])
    # sw_id = int(tmp_switch.name.split("_").pop())
    # block_switch_number = int(sw_id / 8)
    # tmp_switch_value = sw_id % 8

    # self._command_switchs_list[block_switch_number].write_output( chr( 97 + tmp_switch_value )

    # if tmp_switch.is_press:
      # time.sleep(0.2)
      # self._command_switchs_list[block_switch_number].write_output( " " )

    # params["result"] = "OK"

    # return params

  def get_switch_value_handle(self, param):
    #print(param)
    pass

  def set_switch_value_handle(self, param):
    #print(param)
    pass


# units tests
if __name__ == "__main__":
    print("PiControler")
    ctrl = Controler()
    ctrl.do("get_help")
    from time import sleep
    ctrl.start_demo()
    sleep(10)
    ctrl.stop_demo()

# using
# python -m ElectronicControler.PiControler
