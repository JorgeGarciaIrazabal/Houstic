from wshubsapi.Hub import Hub


class HouseHub(Hub):
    def getAllComponents(self, houseId):
        # query components from houseId //maybe sender could be necessary (parent control???)
        return "I am from global server"

    def get_sensor_value(self, sensorId):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        return 0

    def set_sensor_value(self, sensorId):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        return 0

    def __get_house_client(self, componentId):
        # self._getClientsHolder().getClient(lambda x: x.ID = houseID) ...
        return 0