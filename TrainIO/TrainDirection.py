#!/usr/bin/env python

class TrainDirection(object):
    """
Train direction: define the outputs for train management

/---------------------------------------\\
| First Shift Register                  |
| ---------------------------------     |
| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |     |
| ---------------------------------     |
| 1: WaySwitch1_Right  0x10   out8      |
| 2: WaySwitch1_Turn   0x11   out7      |
| 3: WaySwitch2_Right  0x12   out6      |
| 4: WaySwitch2_Turn   0x13   out5      |
| 5: WaySwitch3_Right  0x14   out4      |
| 6: WaySwitch3_Turn   0x15   out3      |
| 7: OnOff_Way         0x16   out2      |
| 8: reserved          0x17   out1      |
|                                       |
| Second Shift Register                 |
| ---------------------------------     |
| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |     |
| ---------------------------------     |
| 1: Park1_Right       0x20   out8      |
| 2: Park1_Turn        0x21   out7      |
| 3: Park2_Right       0x22   out6      |
| 4: Park2_Turn        0x23   out5      |
| 5: Park3_Right       0x24   out4      |
| 6: Park3_Turn        0x25   out3      |
| 7: OnOff_Park1       0x26   out2      |
| 8: OnOff_Park2       0x27   out1      |
\---------------------------------------/

On each register,
the 6 first bits are dedicated to switch,
the 2 lasts bits are dedicated to On off

The modulo 16 defined the register number

    """

    # None
    NOTHING          = 0x00
    
    # First 8bits register
    WAYSWITCH1_RIGHT = 0x10
    WAYSWITCH1_TURN  = 0x11
    WAYSWITCH2_RIGHT = 0x12
    WAYSWITCH2_TURN  = 0x13
    WAYSWITCH3_RIGHT = 0x14
    WAYSWITCH3_TURN  = 0x15
    ONOFF_WAY        = 0x16
    RESERVED         = 0x17
    # Second 8bits register
    PARK1_RIGHT      = 0x20
    PARK1_TURN       = 0x21
    PARK2_RIGHT      = 0x22
    PARK2_TURN       = 0x23
    PARK3_RIGHT      = 0x24
    PARK3_TURN       = 0x25
    ONOFF_PARK1      = 0x26
    ONOFF_PARK2      = 0x27

    # Register list
    first_register = {
            WAYSWITCH1_RIGHT: False,
            WAYSWITCH1_TURN:  False,
            WAYSWITCH2_RIGHT: False,
            WAYSWITCH2_TURN:  False,
            WAYSWITCH3_RIGHT: False,
            WAYSWITCH3_TURN:  False,
            ONOFF_WAY:        False,
            RESERVED:         False
        }

    second_register = {
            PARK1_RIGHT: False,
            PARK1_TURN:  False,
            PARK2_RIGHT: False,
            PARK2_TURN:  False,
            PARK3_RIGHT: False,
            PARK3_TURN:  False,
            ONOFF_PARK1: False,
            ONOFF_PARK2: False
        }
    
    register_list = [first_register, second_register]

    @staticmethod
    def get_value_16bits_register() -> int:
        """
Function: TrainDirection.get_value16bitsregister
Get the both registers to simulate a 16bits shift register
input  : none
output : int -> the concat value for both registers
        """
        return TrainDirection.get_value_8bits_register(TrainDirection.first_register) << 0x08 + \
               TrainDirection.get_value_8bits_register(TrainDirection.second_register)

    @staticmethod
    def get_value_8bits_register(register_hash) -> int:
        """
Function: TrainDirection.get_value_8bits_register
Get the hex value for the 8bit shift register
input  : register_hash -> hash with the definition of train management part
output : int           -> hex value on 8bits
        """
        tuple_value_reg = [(k % 16, register_hash[k]) for k in register_hash.keys()]
        register_calc   = [pow(2,k) for k,v in tuple_value_reg if v]
        return sum(register_calc)

    @staticmethod
    def is_on_off_switch(constant_value) -> bool:
        """
Function: TrainDirection.is_on_off_switch
Return the information of constant_value
if value modulo 16 is greater than 5, it is true
else false
input  : constant_value as int -> the switch to test
output : bool -> result of test
        """
        return constant_value % 16 > 5

    @staticmethod
    def set_value(constant_value, value):
        """
Function: TrainDirection.set_value
Set the needed value to a specific register
input  : constant_value -> the value to change (switch, on_off, ...)
         value          -> boolean
output : none
        """
        
        register_number = int(constant_value / 16) - 1
        if not TrainDirection.is_on_off_switch(constant_value):
            # the switch part only one to true -> reset all other
            for i in range (0, 6):
                TrainDirection.register_list[register_number][int(constant_value / 16) * 16 + i] = False
            if value == False: return
        
        TrainDirection.register_list[register_number][constant_value] = value

        return

    @staticmethod
    def get_value(constant_value) -> bool:
        """
Function: TrainDirection.get_value
Return the actual value from the direction
input  : none
output : bool -> result of the output
        """
        register_number = int(constant_value / 16) - 1
        return bool(TrainDirection.register_list[register_number][constant_value])

    @staticmethod
    def reset_switchs():
        """
Function: TrainDirection.reset_switchs
Reset the switch part on the 8bits register
input  : None
output : None
        """
        TrainDirection.set_value(0x10, False)
        TrainDirection.set_value(0x20, False)
        return

    @staticmethod
    def reset_registers():
        """
Function: TrainDirection.reset_registers
Set to False all values for the both registers
input  : None
output : None
        """
        TrainDirection.reset_switchs()
        for addr in [0x16, 0x17, 0x26, 0x27]:
            TrainDirection.set_value(addr, False)
        return

def unit_tests():
    print(TrainDirection.__doc__)
    print(TrainDirection.get_value_8bits_register.__doc__)

    print(TrainDirection.get_value_16bits_register())

    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.WAYSWITCH1_TURN, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.WAYSWITCH3_TURN, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.ONOFF_WAY, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.PARK1_RIGHT, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.ONOFF_WAY, False)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))

    TrainDirection.set_value(TrainDirection.PARK2_RIGHT, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.WAYSWITCH3_TURN, False)
    print(TrainDirection.get_value_8bits_register(TrainDirection.first_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.PARK3_RIGHT, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.ONOFF_PARK2, True)
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())
    
    TrainDirection.set_value(TrainDirection.PARK3_RIGHT, False)
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.set_value(TrainDirection.ONOFF_PARK2, False)
    print(TrainDirection.get_value_8bits_register(TrainDirection.second_register))
    print(TrainDirection.get_value_16bits_register())

    TrainDirection.reset_registers()
    
if __name__ == '__main__':
    unit_tests()
