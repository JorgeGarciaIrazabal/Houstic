import utils
from config_base import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    def __init__(self):
        self.house_ip = ""  # all available interfaces
        self.house_port = 7159
        self.global_reconnect_timeout = 1
        self.global_ip = "198.100.155.30"  # OVH IP
        self.global_port = 9517
        super(Config, self).__init__()

    def init_config(self):
        self.read_config_file()
        if self.house_ip is None:
            self.house_ip = utils.get_local_ip()
        self.log_config_values()

    def get_global_ws_url(self, id_):
        return "ws://{0}:{1}/{2}".format(self.global_ip, self.global_port, id_)

    def _ignore_attributes(self):
        return super(Config, self)._ignore_attributes() + ["get_global_ws_url"]
