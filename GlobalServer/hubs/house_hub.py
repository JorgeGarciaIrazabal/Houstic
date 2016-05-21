from wshubsapi.hubs_inspector import HubsInspector

from hubs.middle_ware_hub import MiddleWareHub


class HouseHub(MiddleWareHub):
    def list_houses(self):
        return [c.ID for c in self.clients.get_all_clients()]

    def get_all_components(self, house_id):
        # query components from houseId //maybe sender could be necessary (parent control???)
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        components = house.get_components().result()
        return components

    def component_write(self, house_id, module_id, component_key, value):
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        return house.component_write(module_id, component_key, value).result()

    def component_read(self, house_id, module_id, component_key):
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        return house.component_read(module_id, component_key).result()

    def stop_module_communication(self, house_id, module_id):
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        return house.stop_module_communication(module_id).result()

    def reset_module(self, house_id, module_id):
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        return house.reset_module(module_id).result()

    @classmethod
    def get_instance(cls):
        """
        :rtype: HouseHub
        """
        return HubsInspector.get_hub_instance(cls)
