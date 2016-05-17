from hubs.middle_ware_hub import MiddleWareHub


class HouseHub(MiddleWareHub):
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
