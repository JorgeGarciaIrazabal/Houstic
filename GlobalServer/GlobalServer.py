import os
import logging
import logging.config
import json

import sys
from mongoengine import connect
from tornado import web, ioloop
import Hubs

from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.ConnectionHandlers.Tornado import ConnectionHandler

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

settings = {"static_path": os.path.join(os.path.dirname(__file__), "../_static")}

app = web.Application([
    (r'/(.*)', ConnectionHandler),
], **settings)

if __name__ == '__main__':
    connect('houstic' if len(sys.argv) <= 1 else sys.argv[1])
    Hubs.importAllHubs()
    HubsInspector.inspectImplementedHubs()
    HubsInspector.constructJSFile("../Application/HousticApp/www/build/js")
    HubsInspector.constructPythonFile("../LocalServer/libs")
    log.debug("starting...")
    app.listen(9517)

    ioloop.IOLoop.instance().start()