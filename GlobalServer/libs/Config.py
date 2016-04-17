import os
from config_base import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    def __init__(self):
        self.port = 9517
        self.mongo = dict(db="houstic", host=None, port=None, username=None, password=None)
        self.js_client_path = os.path.join(os.pardir, "HousticApp", "app", "libs")
        self.py_client_path = os.path.join(os.pardir, "LocalServer", "libs")
        # super init has to be after declaring attributes to store them correctly
        super(Config, self).__init__()

    def init_config(self):
        self.read_config_file()
        self.log_config_values()

    @classmethod
    def get(cls):
        """ :rtype :Config"""
        return super(Config, cls).get()

