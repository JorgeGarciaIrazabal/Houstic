import logging

import time

import sys
from wshubsapi import Asynchronous

from libs import utils
from libs.ModuleConnection import createSocketServer, ModuleConnection
from libs.WSHubsApi import HubsAPI


class House:
    log = logging.getLogger(__name__)
    HOUSE_IP = utils.getLocalIp()
    HOUSE_PORT = 7159
    GLOBAL_RECONNECT_TIMEOUT = 1
    GLOBAL_SERVER_WS_URL = "ws://{}:9517/1".format(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")

    def __init__(self, ):
        self.globalServerAPI = None
        """:type : HubsAPI """
        # self.componentCommunicationManager
        self.houseServer = createSocketServer(self.HOUSE_IP, self.HOUSE_PORT)
        self.moduleConnections = []
        """:type : list of libs.SocketHandler.SocketHandler"""
        ModuleConnection.onOpen = lambda handler: self.moduleConnections.append(handler)

    @Asynchronous.asynchronous()
    def __autoReconnectGlobalServerAPI(self, *args):
        try:
            self.globalServerAPI = HubsAPI(self.GLOBAL_SERVER_WS_URL)
            self.constructClientAPI()
            self.globalServerAPI.wsClient.closed = self.__autoReconnectGlobalServerAPI
            self.globalServerAPI.connect()
        except:
            self.log.exception("unable to connect to global server")
            time.sleep(self.GLOBAL_RECONNECT_TIMEOUT)
            self.__autoReconnectGlobalServerAPI()

    @Asynchronous.asynchronous()
    def __askAction(self):
        while True:
            text = raw_input("introduce texto: ")
            self.globalServerAPI.HouseHub.client.componentWrite(1, 1 if text == "1" else 0)


    def initializeCommunications(self):
        self.__autoReconnectGlobalServerAPI()
        self.__askAction()
        self.log.debug("house server created")
        self.houseServer.serve_forever()

    def constructClientAPI(self):
        def __getModuleConnection(componentID):
            return self.moduleConnections[0]  # todo find the real module

        def getAllComponents():
            return []

        def componentWrite(componentID, value):
            module = __getModuleConnection(componentID)
            module.writeMessage("W-12-" + str(value))  # mode-pin-value

        def componentRead(componentID):
            return None  # create future when receiving value of sensor

        self.globalServerAPI.HouseHub.client.getAllComponent = getAllComponents
        self.globalServerAPI.HouseHub.client.componentWrite = componentWrite
        self.globalServerAPI.HouseHub.client.componentRead = componentRead

