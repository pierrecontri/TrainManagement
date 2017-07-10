
class SwitchCommand(object):

  # enum the switch state
  ERR = -1
  ON  = 1
  OFF = 0

  def __init__(self, name, group = ""):
    self.name = name
    self.value = SwitchCommand.OFF
    self.group = group

  def switch_value(self):
    if self.value == SwitchCommand.ERR: self.value = SwitchCommand.OFF
    else: self.value = int(not(self.state))
    return

  @property
  def state(self):
    return self.value

  @state.setter
  def state(self, val):
    self.value = val
