if __name__ == "__main__":
    # ---------------- Add Path  --------------------------------------------------
    import sys
    from sys import path as sys_pth
    import os.path as pth
    
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = (
            #local_directory
            pth.realpath(pth.join(local_directory, "..", "TrainLibraries.zip"))
            , pth.realpath(pth.join(local_directory,"..", "Controller"))
            , pth.realpath(pth.join(local_directory,"..", "Model"))
            , pth.realpath(pth.join(local_directory,"..", "ElectronicComponents"))
    )
  
    for to_import in import_list:
        if not pth.exists(to_import): continue
        if not to_import in sys_pth: sys_pth.append(to_import)

    # -----------------------------------------------------------------------------

import threading
from Controller.TrainManagementController import TrainManagementController

from ElectronicComponents import *

import queue
import time

# thread queues list
thread_queues_demo = []

def broadcast_thread_event(data, queue_obj):
    for q in queue_obj: q.put(data)

#broadcast_thread_event = lambda data, queue_obj: (for q in queue_obj: q.put(data))

class Controller(TrainManagementController):
  """
PiController the real controller to manage Raspberry Pi
  """

  def __init__(self):
    self._number_of_switchs_blocks = 3
    TrainManagementController.__init__(self)
    InitGPIO.init_electronic()
    self._shift_register = SN74HC595( inputs_ports = {'ser':5,'oe':6,'rclk':13,'srclk':19,'srclr':26}, outputs_len = 8 * len( self._command_switchs_list ) )
    self._shift_register.allow_output(True)
    for t_cmd_switch in self._command_switchs_list: t_cmd_switch.component_interface = self._shift_register

  @property
  def number_of_switchs_blocks(self):
    return self._number_of_switchs_blocks

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

  def send_message(self, message):
    print("MSG: --%s--" % message)
    return

  def get_switch_value_handle(self, value):
    pass

  def set_switch_value_handle(self, value):
    arr_val = [ (value >> (8 * i)) & 0xff for i in range(0, self.number_of_switchs_blocks) ]
    print("=============")
    print("value: %s" % value)
    print(arr_val)
    return


# units tests
if __name__ == "__main__":
    print("PiController")
    ctrl = Controller()
    ctrl.do("get_help")
    ctrl.set_switch_value_handle(52478561)
    from time import sleep
    ctrl.start_demo()
    sleep(10)
    ctrl.stop_demo()

# using
# python -m ElectronicController.PiController
