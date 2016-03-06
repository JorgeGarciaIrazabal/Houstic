import SocketServer
import logging
from _socket import error

from wshubsapi.utils import MessageSeparator

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SocketHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        # never enter here :O
        self.messageBuffer = ""
        self.__messageSeparator = None
        """:type : MessageSeparator"""

    def setup(self):
        self.__messageSeparator = MessageSeparator()

    def writeMessage(self, message):
        self.request.sendall(message + self.__messageSeparator.sep)

    def handle(self):
        while True:
            try:
                data = self.request.recv(10240)
            except error as e:
                if e.errno == 10054:
                    self.finish()
                    break
            except:
                log.exception("error receiving data")
            else:
                for m in self.__messageSeparator.addData(data):
                    self.handleMessage(m)

    def handleMessage(self, message):
        raise NotImplementedError()

    def finish(self):
        pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def createSocketServer(host, port, SocketHandlerClass=SocketHandler):
    return ThreadedTCPServer((host, port), SocketHandlerClass)
