import logging

from wshubsapi.ConnectionHandlers.Tornado import ConnectionHandler
from wshubsapi.ConnectedClient import ConnectedClient


class HousticClient(ConnectedClient):
    HOUSE, MOBILE = range(2)
    def __init__(self, commEnvironment, writeMessageFunction):
        super(HousticClient, self).__init__(commEnvironment, writeMessageFunction)
        self.device = None


class WSHandler(ConnectionHandler):

    log = logging.getLogger(__name__)

    def __init__(self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)
        self._connectedClient = HousticClient(self.commEnvironment, self.writeMessage)
        """:type: HousticClient"""

    def open(self, device, ID=None, *args):
        try:
            device = int(device)
            if device not in (HousticClient.HOUSE, HousticClient.MOBILE):
                raise Exception("Unable to identify device type: {}".format(device))
        except Exception as e:
            self.close(1, str(e))
            raise
        clientId = ID
        self._connectedClient.device = device

        ID = self.commEnvironment.onOpen(self._connectedClient, clientId)
        self.log.debug("open new connection with ID: {} ".format(ID))
