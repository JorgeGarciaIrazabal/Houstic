import sys
import os

sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, "PythonUtils")]

import hubs
import json
import logging.config
from mongoengine import connect
from tornado import web, ioloop
from wshubsapi import asynchronous
from wshubsapi.hubs_inspector import HubsInspector
import hubs
from hubs.house_hub import HouseHub
from libs.ws_handler import WSHandler
from libs.config import Config
import utils

os.chdir(utils.get_module_path())

logging.config.dictConfig(json.load(open('logging.json')))
log = logging.getLogger(__name__)

settings = {"static_path": os.path.join(os.path.dirname(__file__), "_static")}

app = web.Application([
    (r'/(.*)', WSHandler),
], **settings)


@asynchronous.asynchronous()
def __ask_action():
    while True:
        option = input("introduce value: ")
        house_hub = HubsInspector.get_hub_instance(HouseHub)
        try:
            if option == "0":
                house_hub.component_write(0, '12353AF234', "green", 1)
            elif option == "1":
                house_hub.component_read(0, '12353AF234', 'light')
            else:
                house_hub.get_all_components(0)
        except:
            log.exception("error")


if __name__ == '__main__':
    connect(**Config.get().mongo)
    hubs.import_all_hubs()
    HubsInspector.inspect_implemented_hubs()
    HubsInspector.construct_js_file(Config.get().js_client_path)
    HubsInspector.construct_python_file(Config.get().py_client_path)
    log.debug("starting...")
    app.listen(Config.get().port)
    __ask_action()

    ioloop.IOLoop.instance().start()
