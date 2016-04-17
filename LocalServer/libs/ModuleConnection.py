import SocketServer
import logging
from _socket import error
from concurrent.futures import Future

from wshubsapi.message_separator import MessageSeparator


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

    def __handle_correct_data_received(self, data):
        try:
            for m in self.__messageSeparator.addData(data):
                h, b = m.split(self.headerSeparator)
                self.on_message(h, b, self)
        except:
            self.log.exception(u"error receiving data with message: {}".format(data))

    def setup(self):
        self.log.debug("Connection started in client address: {}".format(self.client_address))
        self.__messageSeparator = MessageSeparator(messageSeparator="~")
        self.headerSeparator = "&&"
        self.future = Future()
        self.ID = None
        ModuleConnection.on_open(self)

    def write_message(self, message):
        """
        :return: Future
        """
        self.request.sendall(message + self.__messageSeparator.separator)
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
                    self.on_close(self)
                    break
                else:
                    raise
            except:
                self.log.exception("error receiving data")
            else:
                self.__handle_correct_data_received(data)

    @staticmethod
    def on_open(handler):
        pass

    @staticmethod
    def on_message(header, body, handler):
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
    def on_close(handler):
        pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def create_socket_server(host, port, socket_handler_class=ModuleConnection):
    return ThreadedTCPServer((host, port), socket_handler_class)
