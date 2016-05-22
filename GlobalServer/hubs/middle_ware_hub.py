from wshubsapi.hub import Hub

from libs.ws_handler import HousticClient


class MiddleWareHub(Hub):
    __HubName__ = None  # setting None, this hub will not be included in the api

    def _get_mobiles(self):
        return self.clients.get(lambda c: c.is_mobile())

    def _get_houses(self):
        return self.clients.get(lambda c: c.is_house())
