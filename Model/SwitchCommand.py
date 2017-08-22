
class SwitchCommand(object):

  # enum the switch state
  ERR = -1
  ON  = 1
  OFF = 0

  def __init__(self, name, group = "", is_press = True, state = 0):
    self._name = name
    self._value = state
    self._group = group
    self._is_press = is_press

  def switch_value(self):
    if self._value == SwitchCommand.ERR: self_.value = SwitchCommand.OFF
    else: self._value = int(not(self._value))
    return self.state

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

  @group.setter
  def group(self, value):
    self._group = value

  def switch_to_json(switch_object):
    return { 'switchName': switch_object.name, 'switchValue': switch_object.state, 'switchGroup': switch_object.group, 'isPersistent': not(switch_object._is_press) }

  def switch_from_json(json_object):
    if "switchName" not in json_object.keys(): raise Exception("SwitchCommand.switch_from_json : json object does not containt switchName parameter")

    sw = SwitchCommand(
            name = json_object["switchName"],
            group = json_object["switchGroup"] if "switchGroup" in json_object.keys() else "_".join(json_object["switchName"].split("_")[0:-2]),
            is_press = not(json_object["isPersistent"]) if "isPersistent" in json_object.keys() else True,
            state = int(json_object["switchValue"]) if "switchValue" in json_object.keys() else SwitchCommand.OFF
         )

    return sw