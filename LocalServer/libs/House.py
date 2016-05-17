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
        self.module_connections = dict()
        """:type : 	Dict from str to ModuleConnection"""
        ModuleConnection.on_open = self.on_module_connected
        ModuleConnection.on_close = self.on_module_closed

    def on_module_connected(self, handler: ModuleConnection):
        self.module_connections[handler.id] = handler
        self.log.debug("module connected")

    def on_module_closed(self, handler):
        self.log.debug("module closed")
        if handler.id in self.module_connections:
            self.module_connections.pop(handler.id)

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
        def get_components():
            modules = dict()
            for id_, module in self.module_connections.items():
                # todo: do this in parallel
                modules[id_] = module.call_in_module("get_components").result()
            return modules

        def component_write(module_id, component_key, value):
            module = self.module_connections[module_id]
            return module.call_in_module("component_write",component_key, value).result()

        def component_read(module_id, component_id):
            module = self.module_connections[module_id]
            return module.call_in_module("component_read", component_id).result()

        self.global_server_api.HouseHub.client.get_components = get_components
        self.global_server_api.HouseHub.client.component_write = component_write
        self.global_server_api.HouseHub.client.component_read = component_read
