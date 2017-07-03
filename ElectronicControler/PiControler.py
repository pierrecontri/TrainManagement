if __name__ == "__main__":
    # ---------------- Add Path  --------------------------------------------------
    import sys
    from sys import path as sys_pth
    import os.path as pth
    
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory,"../Controler")
                        , pth.join(local_directory,"../ElectronicComponents")
                        , pth.join(local_directory,"../ElectronicModel")
    ]
    
    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)
    # -----------------------------------------------------------------------------

import threading
from Controler.TrainManagementControler import TrainManagementControler

import queue

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
    pass

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

  def get_switch_info(self, params):
    params["result"] = "OK"
    return

  def set_switch_value(self, params):
    # add the controler code here
    self.get_switch_info(params)
    return params


def get_controler():
    return Controler()

# units tests
if __name__ == "__main__":
    print("PiControler")
    ctrl = get_controler()
    ctrl.do("get_help")
    from time import sleep
    ctrl.start_demo()
    sleep(10)
    ctrl.stop_demo()

# using
# python -m ElectronicControler.PiControler