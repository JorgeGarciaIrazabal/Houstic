import machine
import json


class Component:
    def __init__(self, name, pin, mode):
        self.pin_num = pin
        self.mode = mode
        self.name = name

    def value(self, *args):
        pass

    def get_info_json(self):
        return dict(pin=self.pin_num, mode=self.mode, value=self.value(), name=self.name)


class DigitalComponent(Component):
    def __init__(self, name, pin, mode):
        super().__init__(name, pin, mode)
        self.pin = machine.Pin(pin, mode)

    def value(self, *args):
        return self.pin.value(*args)


class AnalogInComponent(Component):
    def __init__(self, name, pin, mode):
        super().__init__(name, pin, mode)
        self.pin = machine.ADC(pin)

    def value(self):
        return self.pin.read()


class AnalogOutComponent(Component):
    def __init__(self, name, pin, mode):
        super().__init__(name, pin, mode)
        self.pin = machine.Pin(pin)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(500)
        self.pwm.duty(0)

    def value(self, duty=None):
        if duty is not None:
            return self.pwm.duty(duty)
        return self.pwm.duty()


def construct_component(name, pin, mode):
    if mode == 0 or mode == 1:  # digital_in, digital_out
        return DigitalComponent(name, pin, mode)
    elif mode == 2:  # analog_in
        return AnalogInComponent(name, pin, mode)
    elif mode == 3:  # analog_out
        return AnalogOutComponent(name, pin, mode)


class Api:
    def __init__(self, communication_handler):
        self.components = list()
        self.communication_handler = communication_handler

    def handle(self, message):
        msg_obj = json.loads(str(message))
        function = getattr(self, msg_obj['function'])
        return function(*msg_obj["args"])

    def read_config(self):
        with open("module.init") as f:
            data = json.loads(f.read())
            for component in data["components"]:
                print('constructing: {}'.format(component["name"]))
                self.components.append(construct_component(**component))

    def get_components(self):
        components_dict = [component.get_info_json() for component in self.components]
        return json.dumps(components_dict)

    def component_write(self, index, value):
        component = self.components[index]
        component.value(value)
        return True

    def component_read(self, index):
        component = self.components[index]
        return component.value()

    def reset(self):
        machine.reset()

    def stop_communication(self):
        self.communication_handler.close_communication()
