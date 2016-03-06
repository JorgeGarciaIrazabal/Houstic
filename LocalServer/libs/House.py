import logging

import time
from ws4py.exc import WebSocketException

from wshubsapi import Asynchronous
from libs.SocketHandler import createSocketServer
from libs.WSHubsApi import HubsAPI


class House:
    log = logging.getLogger(__name__)
    HOUSE_IP = "127.0.0.1"
    HOUSE_PORT = 7159
    GLOBAL_RECONNECT_TIMEOUT = 1
    GLOBAL_SERVER_WS_URL = "ws://127.0.0.1:9517/house"

    def __init__(self, ):
        self.globalServerAPI = None
        """:type : HubsAPI """
        # self.componentCommunicationManager
        self.houseServer = createSocketServer(self.HOUSE_IP, self.HOUSE_PORT)

    @Asynchronous.asynchronous()
    def __autoReconnectGlobalServerAPI(self, *args):
        try:
            self.globalServerAPI = HubsAPI(self.GLOBAL_SERVER_WS_URL)
            self.globalServerAPI.wsClient.closed = self.__autoReconnectGlobalServerAPI
            self.globalServerAPI.connect()
        except:
            self.log.exception("unable to connect to global server")
            time.sleep(self.GLOBAL_RECONNECT_TIMEOUT)
            self.__autoReconnectGlobalServerAPI()

    def initializeCommunications(self):
        self.__autoReconnectGlobalServerAPI()
        self.log.debug("house server created")
        self.houseServer.serve_forever()
