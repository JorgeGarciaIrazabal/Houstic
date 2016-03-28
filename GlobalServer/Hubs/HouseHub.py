from Hubs.MiddleWareHub import MiddleWareHub


class HouseHub(MiddleWareHub):
    def getAllComponents(self, houseId):
        # query components from houseId //maybe sender could be necessary (parent control???)
        return dict(component1="cason", component2="casita")

    def getSensorValue(self, componentId):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        return 0

    def setActuatorValue(self, componentId, houseID, value):
        # house = self._getClientsHolder().getClient(lambda x: x.ID = houseID)
        # futures = house.getValueFromSensor(sensorID)
        # return futures[0].result()
        house = self._getClientsHolder().getClient(houseID)
        answer = house.componentWrite(componentId, value).result()
        return answer

    def __getHouseConnection(self, componentId):
        # self._getClientsHolder().getClient(lambda x: x.ID = houseID) ...
        return 0
