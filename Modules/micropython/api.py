import machine
import json


class Component:
    def __init__(self, key, pin, mode):
        self.pin_num = pin
        self.mode = mode
        self.pin = machine.Pin(pin, mode)
        self.key = key


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
                self.components[key] = Component(key, **data)

    def get_components(self):
        components_dict = dict()
        for key, component in self.components.items():
            components_dict[key] = dict(pin=component.pin_num, mode=component.mode)
        return json.dumps(components_dict)

    def component_write(self, key, value):
        component = self.components[key]
        component.pin.value(value)
        return True

    def component_read(self, key):
        component = self.components[key]
        return component.pin.value()

    def reset(self):
        machine.reset()

    def stop_communication(self):
        self.communication_handler.close_communication()
