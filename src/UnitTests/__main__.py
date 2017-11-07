# main for Unit Tests

from sys import path as sys_pth
import os.path as pth
import threading


# GPIO.setwarnings(False)

def demo():
    local_directory = pth.dirname(pth.abspath(__file__))
    import_list = [local_directory
                        , pth.join(local_directory, "..","ElectronicComponents")
                        , pth.join(local_directory, "..","ElectronicModel")
    ]

    for to_import in import_list:
      abs_dir = pth.dirname(pth.abspath(to_import))
      if not abs_dir in sys_pth: sys_pth.append(abs_dir)

    import Time_32OutputsWithMuP as  t32
    import ChaseWithMuP as cwmp

    t_time = threading.Thread( target=t32.time_32outputs, args=() )
    t_chase = threading.Thread( target=cwmp.chase_demo, args=() )

    t_time.daemon = True
    t_chase.daemon = True

    t_time.start()
    t_chase.start()


#demo()