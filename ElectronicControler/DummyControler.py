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

from Controler.TrainManagementControler import TrainManagementControler
import random

class Controler(TrainManagementControler):

    def __init__(self):
        pass

    def get_status(self):
        return { 'Status': 'System OK' }

    def start_demo(self):
        print("DummyDo")
        print((self.get_help())['help'])
        return {'start_demo': 'done'}

    def stop_demo(self):
        return {'stop_demo': 'done'}

    def get_switch_info(self, params):
        params["result"] = "OK" if round(random.random(), 0) == 1 else "NOK"
        return
  
    def set_switch_value(self, params):
        # add the controler code here
        self.get_switch_info(params)
        return params


# units tests
if __name__ == "__main__":
    print("DummyControler")
    ctrl = Controler()
    ctrl.do("get_help")
    from time import sleep
    print("Start Demo: %s" % ctrl.start_demo())
    # sleep(2)
    print("Stop Demo: %s" % ctrl.stop_demo())

# using
# python -m ElectronicControler.DummyControler