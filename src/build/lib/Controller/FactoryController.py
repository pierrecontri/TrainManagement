import sys, os
import re

local_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.realpath(os.path.join(local_directory, "..")) if "TrainLibraries.zip" not in local_directory else os.path.realpath(os.path.join(local_directory, "..", ".."))

# -- Using ElectronicController
class ControllerFactory(object):
    """
    Controller Factory can analyze the driver library presented to the application
    If the driver is transmit as a parameter, it load and return it to the application
    """
    __controller = None

    # used as a singleton
    @classmethod
    def get_controller(cls):
        """
        Cause the physical driver point to electronic component, it must be single
        Used as a singleton
        """
        if cls.__controller is None:
            cls.__controller = cls.instanciate_controller()
        return cls.__controller

    # Create the real controller
    # With specifications in args
    @classmethod
    def instanciate_controller(cls):
        """ Method to select the controller and instantiate it (like a singleton) """
    
        dynamic_controller_name = ""
        if len(sys.argv) > 1:
            dynamic_controller_name = sys.argv[1]

        else:
            # list all files in the plug in controller directory
            lst_controller_files = os.listdir( os.path.realpath(os.path.join(project_directory, "ElectronicController")) )
            # list the possible electronic controllers from the previous list file to filter the controllers
            lstControllers = [re.sub('\.py.?', "", tmpCtrlName) for tmpCtrlName in lst_controller_files if (tmpCtrlName.rfind("Controller") >= 0)]
            print("\nNo Controller sent by parameters, but many controllers detected")
            for pos, elecCtrl in enumerate(lstControllers):
                print("%d: %s" % (pos + 1, elecCtrl))
            print('Please, choose your electronic controller:')
            ctrl_choice = int(sys.stdin.readline().strip())
            ctrl_name = lstControllers[(ctrl_choice - 1) if 0 < ctrl_choice <= len(lstControllers) else 0]
            dynamic_controller_name = "ElectronicController.%s" % ctrl_name
    
        dynamic_controller = __import__(dynamic_controller_name, fromlist=["*"])
        controller = dynamic_controller.Controller()
        # print the controller type
        print("Controller name loaded: %s\n" % dynamic_controller.__name__)
    
        return controller

# -- End Using ElectronicController
