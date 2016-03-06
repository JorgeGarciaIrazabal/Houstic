import os
import logging
import logging.config
import json
from tornado import web, ioloop
import Hubs

from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.ConnectionHandlers.Tornado import ConnectionHandler

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

settings = {"static_path": os.path.join(os.path.dirname(__file__), "../Clients/_static"),}

app = web.Application([
    (r'/(.*)', ConnectionHandler),
], **settings)

if __name__ == '__main__':
    Hubs.importAllHubs()
    HubsInspector.inspectImplementedHubs()
    HubsInspector.constructJSFile("../Application")
    HubsInspector.constructPythonFile("../LocalServer/libs")
    log.debug("starting...")
    app.listen(9517)

    ioloop.IOLoop.instance().start()