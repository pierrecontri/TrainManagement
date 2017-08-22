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
import queue

# thread queues list
thread_queues_demo = []

WAIT_TIME_WRITE_BUS = 0.1

def broadcast_thread_event(data, queue_obj):
    for q in queue_obj:
        q.put(data)

class RSElec(object):

  def __init__(self):
    self.ser_com = serial.Serial(
                 port='COM10', #'/dev/ttyACM0',
                 baudrate=115200,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS
               )
    if not self.ser_com.is_open: self.ser_com.open()

    self.value = 0

  def __del__(self):
    if self.ser_com.is_open: self.ser_com.close()
    del self.ser_com

  def write_output(self, value):
    self.value = value
    print("RSElec write_output: %s" % value)

  def write_msg(self,str_msg):
    self.ser_com.write(str_msg)
    self.ser_com.flushOutput()
    sleep(WAIT_TIME_WRITE_BUS)
    return

  @property
  def hold_value(self) -> int:
    return self.value

rs_elec = RSElec()

class Controler(TrainManagementControler):
  """
PiControler the real controler to manage Raspberry Pi
  """

  _lock = threading.Lock()

  def __init__(self):
    self._number_of_switchs_blocks = 3
    TrainManagementControler.__init__(self)

  @property
  def number_of_switchs_blocks(self):
    return self._number_of_switchs_blocks

  def get_status(self):
    return { 'Status': 'System OK' }


  def start_demo(self):

    def tty_demo(t_queues_demo):
      for j in range (3):
        for i in range(256):
          self.set_switch_value_handle( i << (8*j) )
      self.set_switch_value_handle(0)

    print("start demo")
    thread_queues_demo.clear()
    self.t_chase = threading.Thread( target=tty_demo, args=(thread_queues_demo,) )
    self.t_chase.daemon = True
    self.t_chase.start()
    return {'start_demo': 'done'}

  def stop_demo(self):
    broadcast_thread_event("stop", thread_queues_demo)
    self.t_chase.join()
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
        rs_elec.write_msg((data_msg + '\n').encode('latin1'))

    return

  def get_switch_value_handle(self, value):
    print("ToDo get_switch_value_handle + %s" % value)
    return

  def set_switch_value_handle(self, value):
    print("=============")
    arr_infos = [ str(value >> (y * 8) & 0xff) for y in range(0, self.number_of_switchs_blocks) ]
    info_to_send = "%s;%s" % ( str(self.number_of_switchs_blocks), str(value) )

    # append the command array for RS232 ("SR:>" or "lcdl1:>")
    # send 'SR:>3;1987126688\n'
    send_shift_register = ('SR:>' + info_to_send + '\n').encode('latin1')

    with Controler._lock:
      # send the character to the device
      print(send_shift_register)
      rs_elec.write_msg(send_shift_register)

    send_lcd = ('lcdl2:>' + " ".join(arr_infos) +'\n').encode('latin1')
    
    with Controler._lock:
      # send the character to the device
      print(send_lcd)
      rs_elec.write_msg(send_lcd)

    return

  def get_serial_info(self):
    pass


# units tests
if __name__ == "__main__":
  print("PiControler")
  ctrl = Controler()
  ctrl.do("get_help")
  ctrl.async_send_message("Pont-a-Mousson\n5mm arret")
  sleep(3)
  ctrl.async_send_message("lcd  ready to start real life")
  # ctrl.start_demo()
  # sleep(WAIT_TIME_WRITE_BUS)
  # ctrl.stop_demo()

  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  ctrl.switch_value( {"switchName":"sw1_0", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw1_1").state )
  
  print("s2: %s" % ctrl.get_switch("sw1_1").state )
  ctrl.switch_value( {"switchName":"sw1_1", "switchValue":1} )
  print("s1: %s" % ctrl.get_switch("sw1_0").state )
  print("s2: %s\n" % ctrl.get_switch("sw1_1").state )
  
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  ctrl.switch_value( {"switchName":"sw2_2", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw2_3").state )
  
  print("s4: %s" % ctrl.get_switch("sw2_3").state )
  ctrl.switch_value( {"switchName":"sw2_3", "switchValue":1} )
  print("s3: %s" % ctrl.get_switch("sw2_2").state )
  print("s4: %s\n" % ctrl.get_switch("sw2_3").state )

# using
# python -m ElectronicControler.RSArduinoControler