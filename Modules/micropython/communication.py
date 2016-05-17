import socket
import json


class MessageSeparator:
    DEFAULT_API_SEP = "*API_SEP*"

    def __init__(self, separator=DEFAULT_API_SEP):
        self.buffer = ""
        self.separator = separator

    def parse_data(self, data):
        data = self.buffer + data.decode('utf-8')
        messages = data.split(self.separator)
        self.buffer = messages.pop(-1)
        return messages


class Communication:
    def __init__(self, api, id_, type_):
        self.socket = None
        self.message_separator = MessageSeparator("~")
        self.api = api
        self.type = type_
        self.id = id_

    def _handle_message(self, msg):
        msg_obj = dict(success=True, reply="")
        try:
            msg_obj['reply'] = self.api.handle(msg)
        except Exception as e:
            msg_obj['reply'] = str(e)
            msg_obj['success'] = False
        self.write_message(json.dumps(msg_obj))

    def _send_handshake(self):
        handshake = dict(handshake=True, id=self.id, type=self.type)
        self.write_message(json.dumps(handshake))

    def connect_to_server(self, ip, port):
        address = socket.getaddrinfo(ip, port)[0][-1]
        self.socket = socket.socket()
        self.socket.connect(address)
        self._send_handshake()
        print("connected")

    def write_message(self, message):
        self.socket.send(bytes(message + self.message_separator.separator, 'utf-8'))

    def main_loop(self):
        while True:
            data = self.socket.recv(100)
            if data:
                messages = self.message_separator.parse_data(data)
                for message in messages:
                    self._handle_message(message)
                print(str(data, 'utf8'), end='')
            else:
                break
