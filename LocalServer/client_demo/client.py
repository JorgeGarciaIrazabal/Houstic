
import sys

from wshubsapi.ConnectionHandlers.SocketHandler import SocketClient

if sys.version_info[0] == 2:
    input = raw_input


if __name__ == '__main__':
    s = SocketClient('ws://{}:{}/'.format(sys.argv[1], sys.argv[2]))
    s.connect()

    while True:
        message = input("")
        s.send(message)