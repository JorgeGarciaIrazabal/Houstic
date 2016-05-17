import logging
import time

from wshubsapi import asynchronous

from libs.module_connection import create_socket_server, ModuleConnection
from libs.hubs_api import HubsAPI
from libs.config import Config


class House:
    log = logging.getLogger(__name__)

    def __init__(self, ):
        self.global_server_api = None
        """:type : HubsAPI """
        # self.componentCommunicationManager
        self.house_server = create_socket_server(Config.get().house_ip, Config.get().house_port)
        self.module_connections = []
        """:type : list of ModuleConnection"""
        ModuleConnection.on_open = self.on_module_connected
        ModuleConnection.on_close = self.on_module_closed

    def on_module_connected(self, handler):
        self.module_connections.append(handler)
        self.log.debug("module connected")

    def on_module_closed(self, handler):
        self.log.debug("module closed")
        self.module_connections.remove(handler)

    @asynchronous.asynchronous()
    def __auto_reconnect_global_server_api(self, *args):
        try:
            self.global_server_api = HubsAPI(Config.get().get_global_ws_url(1))
            self.construct_client_api()
            self.global_server_api.ws_client.closed = self.__auto_reconnect_global_server_api
            self.global_server_api.connect()
        except:
            self.log.exception("unable to connect to global server")
            time.sleep(Config.get().global_reconnect_timeout)
            self.__auto_reconnect_global_server_api()

    @asynchronous.asynchronous()
    def __ask_action(self):
        while True:
            text = input("introduce text: ")
            self.global_server_api.HouseHub.client.componentWrite(1, 1 if text == "1" else 0)

    def initialize_communications(self):
        self.__auto_reconnect_global_server_api()
        self.__ask_action()
        self.log.debug("house server created")
        self.house_server.serve_forever()

    def construct_client_api(self):
        def __get_module_connection(component_id):
            try:
                # todo: find module form componentId, m.ID should not be componentID
                return next(m for m in self.module_connections if m.ID == component_id)
            except StopIteration:
                raise Exception("Unable to find component with ID: {}".format(component_id))

        def get_components():
            return self.module_connections[0].call_in_module("get_components").result()

        def component_write(component_id, value):
            module = __get_module_connection(component_id)
            print(module.write_message("W-12-" + str(value)).result())  # mode-pin-value

        def component_read(component_id):
            return None  # create future when receiving value of sensor

        self.global_server_api.HouseHub.client.get_components = get_components
        self.global_server_api.HouseHub.client.component_write = component_write
        self.global_server_api.HouseHub.client.component_read = component_read
