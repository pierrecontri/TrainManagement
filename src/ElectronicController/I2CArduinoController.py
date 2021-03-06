if __name__ == "__main__":
    # ---------------- Add Path  --------------------------------------------------
    import sys
    from sys import path as sys_pth
    import os.path as pth
    
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = (
            local_directory
            , pth.realpath(pth.join(local_directory, "TrainManagement.zip"))
            , pth.realpath(pth.join(local_directory,"../Controller"))
            , pth.realpath(pth.join(local_directory,"../Model"))
            , pth.realpath(pth.join(local_directory,"../ElectronicComponents"))
    )
  
    for to_import in import_list:
        if not os.exists(to_import): continue
        if not to_import in sys_pth: sys_pth.append(to_import)
    # -----------------------------------------------------------------------------

import threading
import smbus
from Controller.TrainManagementController import TrainManagementController

from ElectronicComponents import *

import queue
from time import sleep

# thread queues list
thread_queues_demo = []

DEVICE_ADDRESS = 0x04
BUS_NUMBER = 1
WAIT_TIME_WRITE_BUS = 0.2

def broadcast_thread_event(data, queue_obj):
    for q in queue_obj:
        q.put(data)

class Controller(TrainManagementController):
  """
PiController the real controller to manage Raspberry Pi wiand Arduino by I2C bus
  """

  _lock = threading.Lock()

  def __init__(self):
    self._number_of_switchs_blocks = 3
    TrainManagementController.__init__(self)
    InitGPIO.init_electronic()
    self.slave_addr = DEVICE_ADDRESS
    self.bus = smbus.SMBus(BUS_NUMBER)

  @property
  def number_of_switchs_blocks(self):
    return self._number_of_switchs_blocks

  def get_status(self):
    return { 'Status': 'System OK' }

  def start_demo(self):

    from sys import path as sys_pth
    import os.path as pth

    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = (
            #local_directory
            pth.realpath(pth.join(local_directory, "..", "TrainLibraries.zip"))
            , pth.realpath(pth.join(local_directory, "..", "UnitTests"))
            , pth.realpath(pth.join(local_directory, "..", "ElectronicComponents"))
            , pth.realpath(pth.join(local_directory, "..", "ElectronicModel"))
    )

    for to_import in import_list:
        if not pth.exists(to_import): continue
        if not to_import in sys_pth: sys_pth.append(to_import)

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
    
    if "\n" in message:
      message = ''.join([tmp_msg.ljust(16, ' ') for tmp_msg in message.split('\n')])
    else:
      message = message.ljust(32, ' ')

    data_msg_l1 = [ord(i) for i in "lcdl1:>"] + [ord(j) for j in message[0:16]]
    data_msg_l2 = [ord(i) for i in "lcdl2:>"] + [ord(j) for j in message[16:32]]

    for data_msg in (data_msg_l1, data_msg_l2):
      with Controller._lock:
        self.bus.write_i2c_block_data(self.slave_addr, data_msg[0], data_msg[1:])
        sleep(WAIT_TIME_WRITE_BUS)

    return

  def get_switch_value_handle(self, value):
    pass

  def set_switch_value_handle(self, value):
    arr_val = [ (value >> (8 * i)) & 0xff for i in range(0,self.number_of_switchs_blocks) ]
    print("=============")
    print("value: %s" % value)
    print(arr_val)
    # append the command array for i2c ("SR:>" or "lcdl1:>")
    sendShiftRegister = [ord(i) for i in 'SR:>'] + arr_val
    print(sendShiftRegister)

    with Controller._lock:
      self.bus.write_i2c_block_data(self.slave_addr, sendShiftRegister[0], sendShiftRegister[1:])
      sleep(WAIT_TIME_WRITE_BUS)

    sendLcd = [ord(i) for i in 'lcdl2:>'] + arr_val
    print(sendLcd)
    
    with Controller._lock:
      self.bus.write_i2c_block_data(self.slave_addr, sendLcd[0], sendLcd[1:])
      sleep(WAIT_TIME_WRITE_BUS)

    return


# units tests
if __name__ == "__main__":
    print("PiController")
    ctrl = Controller()
    ctrl.do("get_help")
    ctrl.async_send_message("Pont-a-Mousson\n5mm arret")
    sleep(10)
    ctrl.set_switch_value_handle(52478561)
    ctrl.async_send_message("lcd  ready to start real life")
    ctrl.start_demo()
    sleep(10)
    ctrl.stop_demo()

# using
# python -m ElectronicController.I2CArduinoController
