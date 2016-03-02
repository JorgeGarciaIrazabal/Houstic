import importlib
import json
import logging
import logging.config

from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.ConnectionHandlers.SocketHandler import createSocketServer

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

if __name__ == '__main__':
    HubsInspector.inspectImplementedHubs()
    # HubsInspector.constructPythonFile("../Clients/_static")
    # HubsInspector.constructJSFile("../Clients/_static")

    server = createSocketServer("127.0.0.1", 95173)

    server.serve_forever()


