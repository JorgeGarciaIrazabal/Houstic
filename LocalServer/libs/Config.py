import os
import json
import logging

import sys

from libs import utils


class ConfigException(Exception):
    pass


class Config:
    _log = logging.getLogger(__name__)
    houseIP = "" # all available interfaces
    housePort = 7159
    globalReconnectTimeout = 1
    globalIP = "198.100.155.30" # OVH IP
    globalPort = 9517
    _configFilePath = utils.PROGRAM_PATH + os.sep + ("config.json" if len(sys.argv) == 1 else sys.argv[1])

    @classmethod
    def getGlobalWsURL(cls, id):
        return "ws://{0}:{1}/{2}".format(cls.globalIP,cls.globalPort, id)

    @classmethod
    def getConfigValues(cls):
        configValues = {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
        configValues.pop("getGlobalWsURL")
        configValues.pop("readConfigFile")
        configValues.pop("storeConfigInFile")
        configValues.pop("getConfigValues")
        return configValues

    @classmethod
    def readConfigFile(cls):
        if os.path.exists(cls._configFilePath):
            try:
                cls._log.info("Reading config file")
                with open(cls._configFilePath) as f:
                    jsonObject = json.load(f)
                cls.__dict__.update(jsonObject)
                if cls.houseIP is None:
                    cls.houseIP = utils.getLocalIp()
            except ValueError:
                cls._log.error("Json corrupted so it was ignored, necessary to check!")
        else:
            cls.storeConfigInFile()

    @classmethod
    def storeConfigInFile(cls):
        with open(cls._configFilePath, "w") as f:
            configValues = cls.getConfigValues()
            json.dump(configValues, f, indent=4)
