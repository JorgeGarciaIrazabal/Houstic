import os
import json
import logging
import sys

from libs import utils


class ConfigException(Exception):
    pass


class Config:
    _log = logging.getLogger(__name__)
    port = 9517
    mongo = dict(db="houstic", host=None, port=None, username=None, password=None)
    JSClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "Application", "HousticApp", "app", "libs")
    PyClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "LocalServer", "libs")
    _configFilePath = utils.PROGRAM_PATH + os.sep + ("config.json" if len(sys.argv) == 1 else sys.argv[1])

    @classmethod
    def getGlobalWsURL(cls, id):
        return "ws://{0}:{1}/{2}".format(cls.globalIP, cls.globalPort, id)

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
            except ValueError:
                cls._log.error("Json corrupted so it was ignored, necessary to check!")
        else:
            cls.storeConfigInFile()

    @classmethod
    def storeConfigInFile(cls):
        with open(cls._configFilePath, "w") as f:
            configValues = cls.getConfigValues()
            json.dump(configValues, f, indent=4)
