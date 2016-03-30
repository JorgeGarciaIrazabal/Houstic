import os
import utils
from ConfigBase import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    def __init__(self):
        super(Config, self).__init__()
        self.port = 9517
        self.mongo = dict(db="houstic", host=None, port=None, username=None, password=None)
        self.JSClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "Application", "app", "libs")
        self.PyClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "LocalServer", "libs")

    def initConfig(self):
        self.readConfigFile()
        self.logConfigValues()
