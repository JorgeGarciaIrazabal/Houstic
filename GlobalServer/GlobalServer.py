import os
import logging
import logging.config
import json
import sys

from mongoengine import connect
from tornado import web, ioloop
from wshubsapi import Asynchronous
from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.ConnectionHandlers.Tornado import ConnectionHandler

import Hubs
from Hubs.HouseHub import HouseHub
from libs.Config import Config

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

settings = {"static_path": os.path.join(os.path.dirname(__file__), "_static")}

app = web.Application([
    (r'/(.*)', ConnectionHandler),
], **settings)

@Asynchronous.asynchronous()
def __askAction():
    while True:
        text = raw_input("introduce value: ")
        houseHub = HubsInspector.getHubInstance(HouseHub)
        houseHub.setActuatorValue("Caldera", 1 if text == "1" else 0)


if __name__ == '__main__':
    Config.readConfigFile()
    connect(**Config.mongo)
    Hubs.importAllHubs()
    HubsInspector.inspectImplementedHubs()
    HubsInspector.constructJSFile(Config.JSClientPath)
    HubsInspector.constructPythonFile(Config.PyClientPath)
    log.debug("starting...")
    app.listen(Config.port)
    __askAction()

    ioloop.IOLoop.instance().start()