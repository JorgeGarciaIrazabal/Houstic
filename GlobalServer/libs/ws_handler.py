import logging

from wshubsapi.connection_handlers.tornado_handler import ConnectionHandler
from wshubsapi.connected_client import ConnectedClient
from enums import ClientType


class HousticClient(ConnectedClient):
    def __init__(self, comm_environment, write_msg_function, ip):
        super(HousticClient, self).__init__(comm_environment, write_msg_function)
        self.device = None
        self.ip = ip

    def is_house(self):
        return self.device == ClientType.HOUSE

    def is_mobile(self):
        return self.device == ClientType.MOBILE


class WSHandler(ConnectionHandler):
    log = logging.getLogger(__name__)

    def __init__(self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)
        self._connected_client = HousticClient(self.comm_environment, self.write_message, request.remote_ip)
        """:type: HousticClient"""

    def open(self, device, id_=None, *args):
        try:
            device = ClientType(int(device))
        except Exception as e:
            self.close(1, str(e))
            raise
        client_id = id_
        self._connected_client.device = device

        id_ = self.comm_environment.on_opened(self._connected_client, client_id)
        self.log.debug("open new connection with ID: {} ".format(id_))
