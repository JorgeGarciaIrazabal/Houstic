try:
    import SocketServer as socketserver
except ImportError:
    import socketserver
import logging
from _socket import error
from concurrent.futures import Future
import json

from wshubsapi.message_separator import MessageSeparator


class ModuleConnection(socketserver.BaseRequestHandler):
    log = logging.getLogger(__name__)
    log.addHandler(logging.NullHandler())

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        # never enter here :O
        self.message_buffer = ""
        self._message_separator = None
        """:type : MessageSeparator"""
        self.future = None
        """:type : Future"""
        self.id = None
        self.type = None

    def __handle_correct_data_received(self, data):
        try:
            for message in self._message_separator.add_data(data):
                self.on_message(json.loads(message))
        except Exception as e:
            self.future.set_exception(e)
            self.log.exception(u"error receiving data with message: {}".format(data))

    def setup(self):
        self.log.debug("Connection started in client address: {}".format(self.client_address))
        self._message_separator = MessageSeparator(separator="~")
        self.future = Future()
        self.id = None

    def call_in_module(self, function_name, *args) -> Future:
        msg = dict(function=function_name, args=args)
        self.request.sendall(bytes(json.dumps(msg) + self._message_separator.separator, 'utf-8'))
        self.future = Future()
        return self.future

    def write_message(self, message) -> Future:
        self.request.sendall(message + self._message_separator.separator)
        self.future = Future()
        return self.future

    def handle(self):
        while True:
            try:
                data = self.request.recv(10240)
                if data == "" or data == b'':
                    self.log.warning("connection closed")
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

    def on_message(self, msg_obj):
        if "handshake" in msg_obj:
            self.type = msg_obj['type']
            self.id = msg_obj['id']
            ModuleConnection.on_open(self)
        elif msg_obj['success']:
            self.future.set_result(msg_obj["reply"])
        else:
            self.future.set_exception(Exception(msg_obj["reply"]))

    @staticmethod
    def on_close(handler):
        pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def create_socket_server(host, port, socket_handler_class=ModuleConnection):
    return ThreadedTCPServer((host, port), socket_handler_class)
