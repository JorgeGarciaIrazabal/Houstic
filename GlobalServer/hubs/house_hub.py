import json
from wshubsapi.hubs_inspector import HubsInspector
from wshubsapi.utils_api_hub import UtilsAPIHub

from db.house_model import House
from hubs.middle_ware_hub import MiddleWareHub


class HouseHub(MiddleWareHub):
    def list_houses(self):
        return_houses = []
        connected_houses = {h.ID: h.ip for h in self._get_houses()}
        for house in House.objects:
            house_dict = json.loads(house.to_json())
            house_dict["id"] = str(house.id)
            house_dict["connected"] = house_dict["id"] in connected_houses

            house_dict["ip"] = connected_houses[house_dict["id"]] if house_dict["connected"] else ""
            return_houses.append(house_dict)
        return return_houses

    # def get_all_components(self, house_id):
    #     house = self.clients.get(house_id)
    #     components = house.get_components().result()
    #     return components
    #
    # def component_write(self, house_id, module_id, component_key, value):
    #     house = self.clients.get(house_id)
    #     return house.component_write(module_id, component_key, value).result()
    #
    # def component_read(self, house_id, module_id, component_key):
    #     house = self.clients.get(house_id)
    #     return house.component_read(module_id, component_key).result()
    #
    # def stop_module_communication(self, house_id, module_id):
    #     house = self.clients.get(house_id)
    #     return house.stop_module_communication(module_id)
    #
    # def reset_module(self, house_id, module_id):
    #     house = self.clients.get(house_id)
    #     return house.reset_module(module_id).result()

    def create(self, _sender):
        house = House()
        house.save()
        id_ = str(house.id)

        api_hub = HubsInspector.get_hub_instance(UtilsAPIHub)
        api_hub.set_id(id_, _sender)
        return id_

    def update(self, house_info):
        house = House.objects(id=house_info["id"]).get()
        house.name = house_info["name"]
        house.icon = house_info["icon"]
        house.save()

    @classmethod
    def get_instance(cls):
        """
        :rtype: HouseHub
        """
        return HubsInspector.get_hub_instance(cls)

    def _define_client_functions(self):
        return dict(get_modules=lambda: None,
                    component_write=lambda module_id, component_index, value: None,
                    component_read=lambda module_id, component_index: None,
                    reset_module=lambda module_id: None,
                    stop_module_communication=lambda module_id: None)
