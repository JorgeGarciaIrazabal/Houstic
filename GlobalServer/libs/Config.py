import os
from ConfigBase import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    def __init__(self):
        self.port = 9517
        self.mongo = dict(db="houstic", host=None, port=None, username=None, password=None)
        self.JSClientPath = os.path.join(os.pardir, "HousticApp", "app", "libs")
        self.PyClientPath = os.path.join(os.pardir, "LocalServer", "libs")
        # super init has to be after declaring attributes to store them correctly
        super(Config, self).__init__()

    def initConfig(self):
        self.readConfigFile()
        self.logConfigValues()
