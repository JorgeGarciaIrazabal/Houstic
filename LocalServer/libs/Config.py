import utils
from ConfigBase import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    houseIP = "" # all available interfaces
    housePort = 7159
    globalReconnectTimeout = 1
    globalIP = "198.100.155.30" # OVH IP
    globalPort = 9517

    @classmethod
    def initConfig(cls):
        cls.readConfigFile()
        if cls.houseIP is None:
            cls.houseIP = utils.getLocalIp()
        cls.logConfigValues()

    @classmethod
    def getGlobalWsURL(cls, id):
        return "ws://{0}:{1}/{2}".format(cls.globalIP, cls.globalPort, id)

    @classmethod
    def _ignoreAttributes(cls):
        return ConfigBase._ignoreAttributes() + ["getGlobalWsURL"]


