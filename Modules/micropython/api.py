import machine
import json


class Component:
    def __init__(self, key, pin, mode):
        self.pin_num = pin
        self.mode = mode
        self.key = key

    def value(self, *args):
        pass


class DigitalComponent(Component):
    def __init__(self, key, pin, mode):
        super().__init__(key, pin, mode)
        self.pin = machine.Pin(pin, mode)

    def value(self, *args):
        return self.pin.value(*args)


class AnalogInComponent(Component):
    def __init__(self, key, pin, mode):
        super().__init__(key, pin, mode)
        self.pin = machine.ADC(pin)

    def value(self):
        return self.pin.read()


class AnalogOutComponent(Component):
    def __init__(self, key, pin, mode):
        super().__init__(key, pin, mode)
        self.pin = machine.Pin(pin)
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(500)
        self.pwm.duty(0)

    def value(self, duty=None):
        if duty is not None:
            return self.pwm.duty(duty)
        return self.pwm.duty()


def construct_component(key, pin, mode):
    if mode == 0 or mode == 1:  # digital_in, digital_out
        return DigitalComponent(key, pin, mode)
    elif mode == 2:  # analog_in
        return AnalogInComponent(key, pin, mode)
    elif mode == 3:  # analog_out
        return AnalogOutComponent(key, pin, mode)


class Api:
    def __init__(self, communication_handler):
        self.components = dict()
        self.communication_handler = communication_handler

    def handle(self, message):
        msg_obj = json.loads(str(message))
        function = getattr(self, msg_obj['function'])
        return function(*msg_obj["args"])

    def read_config(self):
        with open("module.init") as f:
            data = json.loads(f.read())
            for key, data in data["components"].items():
                print('constructing: {}'.format(key))
                self.components[key] = construct_component(key, **data)

    def get_components(self):
        components_dict = dict()
        for key, component in self.components.items():
            components_dict[key] = dict(pin=component.pin_num, mode=component.mode, value=component.value())
        return json.dumps(components_dict)

    def component_write(self, key, value):
        component = self.components[key]
        component.value(value)
        return True

    def component_read(self, key):
        component = self.components[key]
        return component.value()

    def reset(self):
        machine.reset()

    def stop_communication(self):
        self.communication_handler.close_communication()
