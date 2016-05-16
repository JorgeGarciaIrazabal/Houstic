import socket


class MessageSeparator:
    DEFAULT_API_SEP = "*API_SEP*"

    def __init__(self, separator=DEFAULT_API_SEP):
        self.buffer = ""
        self.separator = separator

    def parse_data(self, data):
        data = self.buffer + data
        messages = data.split(self.separator)
        self.buffer = messages.pop(-1)
        return messages



class Communication:
    def __init__(self):
        self.socket = None
        self.message_separator = MessageSeparator()
        self.api = None

    def connect_to_server(self, ip, port):
        address = socket.getaddrinfo(ip, port)[0][-1]
        self.socket = socket.socket()
        self.socket.connect(address)

    def write_message(self, message):
        self.socket.send(bytes(message, 'utf-8'))

    def main_loop(self):
        while True:
            data = self.socket.recv(100)
            if data:
                messages = self.message_separator.parse_data(data)
                for message in messages:
                    self.api.handle(message)
                print(str(data, 'utf8'), end='')
            else:
                break
