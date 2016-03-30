import utils
from ConfigBase import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):


    def __init__(self):
        self.houseIP = "" # all available interfaces
        self.housePort = 7159
        self.globalReconnectTimeout = 1
        self.globalIP = "198.100.155.30" # OVH IP
        self.globalPort = 9517
        super(Config, self).__init__()

    def initConfig(self):
        self.readConfigFile()
        if self.houseIP is None:
            self.houseIP = utils.getLocalIp()
        self.logConfigValues()


    def getGlobalWsURL(self, ID):
        return "ws://{0}:{1}/{2}".format(self.globalIP, self.globalPort, ID)

    def _ignoreAttributes(self):
        return super(Config, self)._ignoreAttributes() + ["getGlobalWsURL"]


