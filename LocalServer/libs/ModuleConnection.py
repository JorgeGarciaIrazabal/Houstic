import SocketServer
import logging
from _socket import error

from concurrent.futures._base import Future
from wshubsapi import Asynchronous
from wshubsapi.utils import MessageSeparator


class ModuleConnection(SocketServer.BaseRequestHandler):
    log = logging.getLogger(__name__)
    log.addHandler(logging.NullHandler())

    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        # never enter here :O
        self.messageBuffer = ""
        self.__messageSeparator = None
        """:type : MessageSeparator"""
        self.headerSeparator = None
        self.future = None
        self.ID = None

    def __handleCorrectDataReceived(self, data):
        try:
            for m in self.__messageSeparator.addData(data):
                h, b = m.split(self.headerSeparator)
                self.onMessage(h, b, self)
        except:
            self.log.exception(u"error receiving data with message: {}".format(data))

    def setup(self):
        self.log.debug("Connection started in client address: {}".format(self.client_address))
        self.__messageSeparator = MessageSeparator(messageSeparator="~")
        self.headerSeparator = "&&"
        self.future = Future()
        self.ID = None
        ModuleConnection.onOpen(self)

    def writeMessage(self, message):
        """
        :return: Future
        """
        self.request.sendall(message + self.__messageSeparator.sep)
        self.future = Future()
        return self.future

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
                else:
                    raise
            except:
                self.log.exception("error receiving data")
            else:
                self.__handleCorrectDataReceived(data)

    @staticmethod
    def onOpen(handler):
        pass

    @staticmethod
    def onMessage(header, body, handler):
        if header == "RESULT":
            if body == "SUCCESS":
                handler.future.set_result(True)
            else:
                handler.future.set_exception(Exception("Error setting executing action"))
        elif header == "ID":
            handler.ID = body
            # todo: we need to extend this hello message receiving:
            # - moduleID
            # components list with:
            #  digital/analog
            #  input/output
            #  componentID
            #  realPin? this might be responsibility of the module

    @staticmethod
    def onClose(handler):
        pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def createSocketServer(host, port, SocketHandlerClass=ModuleConnection):
    return ThreadedTCPServer((host, port), SocketHandlerClass)
