import machine
import json


class Component:
    def __init__(self, pin, mode, name):
        self.pin_num = pin
        self.mode = mode
        self.pin = machine.Pin(pin, mode)
        self.name = name


class Api:
    def __init__(self):
        self.components = dict()

    def handle(self, message):
        msg_obj = json.loads(str(message))
        function = getattr(self, msg_obj['function'])
        return function(*msg_obj["args"])

    def read_config(self):
        with open("module.init") as f:
            data = json.loads(f.read())
            for component in data["components"]:
                self.components[component["name"]] = Component(**component)

    def get_components(self):
        components_dict = dict()
        for key, component in self.components.items():
            components_dict[key] = dict(pin=component.pin_num, mode=component.mode)
        return json.dumps(components_dict)


