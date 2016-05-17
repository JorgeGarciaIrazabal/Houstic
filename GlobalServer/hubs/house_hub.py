from hubs.middle_ware_hub import MiddleWareHub


class HouseHub(MiddleWareHub):
    def get_all_components(self, house_id):
        # query components from houseId //maybe sender could be necessary (parent control???)
        house = self.clients.get_all_clients()[0]  # todo: use house_id
        components = house.get_components().result()
        return components

    def get_sensor_value(self, component_id):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        return 0

    def set_actuator_value(self, component_id, house_id, value):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        house = self.clients.getClient(house_id)
        answer = house.componentWrite(component_id, value).result()
        return answer

    def __get_house_connection(self, component_id):
        # self._getClientsHolder().getClient(lambda x: x.ID = houseID) ...
        return 0
