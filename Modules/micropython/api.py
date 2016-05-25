import machine
import json


class Api:
    def __init__(self, module):
        self.module = module
        self.communication_handler = module.communication_handler

    def handle(self, message):
        msg_obj = json.loads(str(message))
        function = getattr(self, msg_obj['function'])
        return function(*msg_obj["args"])

    def get_components(self):
        components_dict = [component.get_info_json() for component in self.module.components]
        return json.dumps(components_dict)

    def component_write(self, index, value):
        component = self.module.components[index]
        component.value(value)
        return True

    def component_read(self, index):
        component = self.module.components[index]
        return component.value()

    def reset(self):
        machine.reset()

    def stop_communication(self):
        self.communication_handler.close_communication()
