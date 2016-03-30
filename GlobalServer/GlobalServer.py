import sys
import os
sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, "PythonUtils")]

import json
import logging.config

from mongoengine import connect
from tornado import web, ioloop
from wshubsapi import Asynchronous
from wshubsapi.HubsInspector import HubsInspector

import Hubs
from Hubs.HouseHub import HouseHub
from libs.WSHandler import WSHandler
from libs.Config import Config

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

settings = {"static_path": os.path.join(os.path.dirname(__file__), "_static")}

app = web.Application([
    (r'/(.*)', WSHandler),
], **settings)

@Asynchronous.asynchronous()
def __askAction():
    while True:
        text = raw_input("introduce value: ")
        houseHub = HubsInspector.getHubInstance(HouseHub)
        houseHub.setActuatorValue("Caldera", 1 if text == "1" else 0)


if __name__ == '__main__':
    connect(**Config.get().mongo)
    Hubs.importAllHubs()
    HubsInspector.inspectImplementedHubs()
    HubsInspector.constructJSFile(Config.get().JSClientPath)
    HubsInspector.constructPythonFile(Config.get().PyClientPath)
    log.debug("starting...")
    app.listen(Config.get().port)
    __askAction()

    ioloop.IOLoop.instance().start()