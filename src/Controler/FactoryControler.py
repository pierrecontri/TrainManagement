import sys, os
import re

local_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.realpath(os.path.join(local_directory, "..")) if "TrainLibraries.zip" not in local_directory else os.path.realpath(os.path.join(local_directory, "..", ".."))

# -- Using ElectronicControler
class ControlerFactory(object):
    """
    Controler Factory can analyse the driver library presented to the application
    If the driver is transmit as a parameter, it load and return it to the application
    """
    __controler = None

    # used as a singleton
    @classmethod
    def get_controler(cls):
        """
        Cause the physical driver point to electronic composant, it must be single
        Used as a singleton
        """
        if cls.__controler is None:
            cls.__controler = cls.instanciate_controler()
        return cls.__controler

    # Create the real controler
    # With specifications in args
    @classmethod
    def instanciate_controler(cls):
        """ Method to select the controler and instanciate it (like a singleton) """
    
        dynamic_controler_name = ""
        if len(sys.argv) > 1:
            dynamic_controler_name = sys.argv[1]
        else:
            # list the possible electronic controlers
            lstControlers = [re.sub('\.py.?', "", tmpCtrlName) for tmpCtrlName in os.listdir(os.path.realpath(os.path.join(project_directory, "ElectronicControler"))) if (tmpCtrlName.rfind("Controler") >= 0)]
            print("\nNo Controler sent by parameters, but many controlers detected")
            for pos, elecCtrl in enumerate(lstControlers):
                print("%d: %s" % (pos + 1, elecCtrl))
            print('Please, choose your electronic controler:')
            ctrl_choice = int(sys.stdin.readline().strip())
            ctrl_name = lstControlers[(ctrl_choice - 1) if 0 < ctrl_choice <= len(lstControlers) else 0]
            dynamic_controler_name = "ElectronicControler.%s" % ctrl_name
    
        dynamic_controler = __import__(dynamic_controler_name, fromlist=["*"])
        controler = dynamic_controler.Controler()
        # print the controler type
        print("Controler name loaded: %s\n" % dynamic_controler.__name__)
    
        return controler

# -- End Using ElectronicControler
