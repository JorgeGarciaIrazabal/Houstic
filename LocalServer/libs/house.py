import json
import logging
import time
from wshubsapi import asynchronous
from libs.module_connection import create_socket_server, ModuleConnection
from libs.hubs_api import HubsAPI
from libs.config import Config


class House(HubsAPI.HouseHubClass.ClientClass):
    log = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.global_server_api = None
        """:type : HubsAPI """
        # self.componentCommunicationManager
        self.house_server = create_socket_server(Config.get().house_ip, Config.get().house_port)
        self.module_connections = dict()
        """:type : 	Dict from str to ModuleConnection"""
        ModuleConnection.on_open = self.on_module_connected
        ModuleConnection.on_close = self.on_module_closed

    def _get_module(self, id_):
        if id_ in self.module_connections:
            return self.module_connections[id_]
        else:
            raise Exception("No module with id: {}".format(id_))

    def on_module_connected(self, handler: ModuleConnection):
        self.module_connections[handler.id] = handler
        self.log.info("module connected")

    def on_module_closed(self, handler):
        self.log.warning("module closed")
        if handler.id in self.module_connections:
            self.module_connections.pop(handler.id)

    @asynchronous.asynchronous()
    def __auto_reconnect_global_server_api(self, *args):
        try:
            self.global_server_api = HubsAPI(Config.get().get_global_ws_url())
            # telling hubs api I am the houseHub client
            self.global_server_api.HouseHub.client = self
            self.global_server_api.ws_client.closed = self.__auto_reconnect_global_server_api
            self.global_server_api.connect()
            if Config.get().id is None:
                self.log.info("asking for ID")
                Config.get().id = self.global_server_api.HouseHub.server.create().result()
                Config.get().store_config_in_file()
                self.log.info("stored ID: {}".format(Config.get().id))
        except:
            self.log.error('Server connection lost')
            time.sleep(Config.get().global_reconnect_timeout)
            self.__auto_reconnect_global_server_api()

    def initialize_communications(self):
        self.__auto_reconnect_global_server_api()
        self.log.debug("house server created")
        self.house_server.serve_forever()

    ################
    #  Client api  #
    ################

    def get_components(self, ):
        modules_info = list()
        for id_, module in self.module_connections.items():
            # todo: do this in parallel
            module_info = dict()
            module_info["components"] = json.loads(module.call_in_module("get_components").result())
            module_info["id"] = id_
            modules_info.append(module_info)
        return modules_info

    def component_write(self, module_id, component_index, value):
        module = self._get_module(module_id)
        return module.call_in_module("component_write", component_index, value).result()

    def component_read(self, module_id, component_index):
        module = self._get_module(module_id)
        return module.call_in_module("component_read", component_index).result()

    def reset_module(self, module_id):
        module = self._get_module(module_id)
        return module.call_in_module("reset").result()

    def stop_module_communication(self, module_id):
        module = self._get_module(module_id)
        return module.call_in_module("stop_communication").result()

