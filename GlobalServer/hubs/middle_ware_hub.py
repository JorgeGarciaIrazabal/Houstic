from wshubsapi.hub import Hub

from libs.ws_handler import HousticClient


class MiddleWareHub(Hub):
    __HubName__ = None  # setting None, this hub will not be included in the api

    def _get_mobiles(self, func):
        def filter_function(client):
            return client.device == HousticClient.MOBILE and func(client)

        return self._getClientsHolder().getClients(filter_function)

    def _get_houses(self, func):
        def filter_function(client):
            return client.device == HousticClient.HOUSE and func(client)

        return self._getClientsHolder().getClients(filter_function)
