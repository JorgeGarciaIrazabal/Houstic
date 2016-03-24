import logging
import time

from wshubsapi import Asynchronous

from libs.ModuleConnection import createSocketServer, ModuleConnection
from libs.WSHubsApi import HubsAPI
from Config import Config


class House:
    log = logging.getLogger(__name__)

    def __init__(self, ):
        self.globalServerAPI = None
        """:type : HubsAPI """
        # self.componentCommunicationManager
        self.houseServer = createSocketServer(Config.houseIP, Config.housePort)
        self.moduleConnections = []
        """:type : list of libs.SocketHandler.SocketHandler"""
        ModuleConnection.onOpen = lambda handler: self.moduleConnections.append(handler)

    @Asynchronous.asynchronous()
    def __autoReconnectGlobalServerAPI(self, *args):
        try:
            self.globalServerAPI = HubsAPI(Config.getGlobalWsURL(1))
            self.constructClientAPI()
            self.globalServerAPI.wsClient.closed = self.__autoReconnectGlobalServerAPI
            self.globalServerAPI.connect()
        except:
            self.log.exception("unable to connect to global server")
            time.sleep(Config.globalReconnectTimeout)
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
            try:
                return next(m for m in self.moduleConnections if m.name==componentID)
            except StopIteration:
                raise Exception("Unable to find component with ID: {}".format(componentID))

        def getAllComponents():
            return []

        def componentWrite(componentID, value):
            module = __getModuleConnection(componentID)
            print module.writeMessage("W-12-" + str(value)).result()  # mode-pin-value

        def componentRead(componentID):
            return None  # create future when receiving value of sensor

        self.globalServerAPI.HouseHub.client.getAllComponent = getAllComponents
        self.globalServerAPI.HouseHub.client.componentWrite = componentWrite
        self.globalServerAPI.HouseHub.client.componentRead = componentRead

