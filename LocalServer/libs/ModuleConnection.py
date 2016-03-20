import SocketServer
import logging
from _socket import error

from wshubsapi import Asynchronous
from wshubsapi.utils import MessageSeparator


class ModuleConnection(SocketServer.BaseRequestHandler):
    log = logging.getLogger(__name__)
    log.addHandler(logging.NullHandler())

    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        # never enter here :O
        self.messageBuffer = ""
        self.onOpen = lambda handler: None
        self.onMessage = lambda message, handler: None
        self.onClose = lambda handler: None
        self.__messageSeparator = None
        """:type : MessageSeparator"""

    def setup(self):
        self.log.debug("Connection started in client address: {}".format(self.client_address))
        self.__messageSeparator = MessageSeparator(messageSeparator="~")
        ModuleConnection.onOpen(self)

    def writeMessage(self, message):
        self.request.sendall(message + self.__messageSeparator.sep)

    def handle(self):
        while True:
            try:
                data = self.request.recv(10240)
                if data == "":
                    return
                self.log.debug("received: {}".format(data))
            except error as e:
                if e.errno == 10054:
                    self.onClose(self)
                    break
            except:
                self.log.exception("error receiving data")
            else:
                for m in self.__messageSeparator.addData(data):
                    self.onMessage(m, self)

    @staticmethod
    def onOpen(handler):
        pass

    @staticmethod
    def onMessage(self, message, handler):
        pass

    @staticmethod
    def onClose(self, handler):
        pass




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def createSocketServer(host, port, SocketHandlerClass=ModuleConnection):
    return ThreadedTCPServer((host, port), SocketHandlerClass)
