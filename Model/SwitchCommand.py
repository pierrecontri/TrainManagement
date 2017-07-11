
class SwitchCommand(object):

  # enum the switch state
  ERR = -1
  ON  = 1
  OFF = 0

  def __init__(self, name, group = "", is_press= True):
    self._name = name
    self._value = SwitchCommand.OFF
    self._group = group
    self._is_press = is_press

  def switch_value(self):
    if self._value == SwitchCommand.ERR: self_.value = SwitchCommand.OFF
    else: self._value = int(not(self._value))
    return

  @property
  def state(self):
    return self._value

  @state.setter
  def state(self, val):
    self._value = val

  @property
  def is_press(self):
    return self._is_press

  @property
  def name(self):
    return self._name

  @property
  def group(self):
    return self._group