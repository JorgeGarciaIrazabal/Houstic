from wshubsapi.Hub import Hub

from libs.WSHandler import HousticClient


class MiddleWareHub(Hub):
    __HubName__ = None # setting None, this hub will not be included in the api

    def _getMobiles(self, func):
        def filterFunction(client):
            return client.device == HousticClient.MOBILE and func(client)

        return self._getClientsHolder().getClients(filterFunction)

    def _getHouses(self, func):
        def filterFunction(client):
            return client.device == HousticClient.HOUSE and func(client)

        return self._getClientsHolder().getClients(filterFunction)