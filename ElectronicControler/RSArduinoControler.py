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

import threading
import serial
from Controler.TrainManagementControler import TrainManagementControler
from time import sleep

WAIT_TIME_WRITE_BUS = 0.2

class Controler(TrainManagementControler):
  """
PiControler the real controler to manage Raspberry Pi
  """

  _lock = threading.Lock()

  def __init__(self):
    self._number_of_switchs_blocks = 3
    TrainManagementControler.__init__(self)
    self.serial = serial.Serial(
                 port='COM10', #'/dev/ttyACM0',
                 baudrate=115200,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS
               )
    if not self.serial.is_open: self.serial.open()

  def __del__(self):
    if self.serial.is_open: self.serial.close()
    del self.serial

  @property
  def number_of_switchs_blocks(self):
    return self._number_of_switchs_blocks

  def get_status(self):
    return { 'Status': 'System OK' }

  def start_demo(self):

    return {'start_demo': 'done'}

  def stop_demo(self):

    return {'stop_demo': 'done'}

  def send_message(self, message):
    
    if "\n" in message:
        message = ''.join([tmp_msg.ljust(16, ' ') for tmp_msg in message.split('\n')])
    else:
      message = message.ljust(32, ' ')

    data_msg_l1 = "lcdl1:>" + message[0:16]
    data_msg_l2 = "lcdl2:>" + message[16:32]

    for data_msg in (data_msg_l1, data_msg_l2):
      with Controler._lock:
        self.serial.write((data_msg + '\n').encode('latin1'))
        sleep(WAIT_TIME_WRITE_BUS)

    return

  def get_switch_value_handle(self, value):
    pass

  def set_switch_value_handle(self, value):
    arr_val = [ (value >> (8 * i)) & 0xff for i in range(0,self.number_of_switchs_blocks) ]
    print("=============")
    print("value: %s" % value)
    print(arr_val)
    # append the command array for RS232 ("SR:>" or "lcdl1:>")
    #sendShiftRegister = ('SR:>' + "".join([chr(i) for i in arr_val]) + '\n').encode('latin1')
    # send 'SR:>3,1987126688\n'
    sendShiftRegister = ('SR:>' + str(self.number_of_switchs_blocks) + ',' + str(value) + '\n').encode('latin1')

    with Controler._lock:
      # send the character to the device
      print(sendShiftRegister)
      self.serial.write(sendShiftRegister)
      self.serial.flushOutput()
      sleep(WAIT_TIME_WRITE_BUS)

    sendLcd = ('lcdl2:>' + "".join([chr(i) for i in arr_val]) +'\n').encode('latin1')
    
    with Controler._lock:
      # send the character to the device
      print(sendLcd)
      self.serial.write(sendLcd)
      self.serial.flushOutput()
      sleep(WAIT_TIME_WRITE_BUS)

    return

  def get_serial_info(self):
    return self.serial.readall()


# units tests
if __name__ == "__main__":
    print("PiControler")
    ctrl = Controler()
    ctrl.do("get_help")
    ctrl.async_send_message("Pont-a-Mousson\n5mm arret")

    ctrl.set_switch_value_handle(52478561)
    #print(ctrl.get_serial_info())
    sleep(3)
    ctrl.set_switch_value_handle(20)
    sleep(3)
    ctrl.set_switch_value_handle(167)
    sleep(3)

    ctrl.set_switch_value_handle(0)
    sleep(3)

    for j in range (0,3):
      for i in range(0, 20):
        ctrl.set_switch_value_handle( i << (8*j) )
        sleep(0.2)

    ctrl.set_switch_value_handle(0)
    sleep(3)
    ctrl.async_send_message("lcd  ready to start real life")
    ctrl.start_demo()
    sleep(3)
    ctrl.stop_demo()

# using
# python -m ElectronicControler.RSArduinoControler