import os
import json
import logging
import sys

import utils


class ConfigException(Exception):
    pass


class ConfigBase:
    _log = logging.getLogger(__name__)
    _configFilePath = utils.PROGRAM_PATH + os.sep + ("config.json" if len(sys.argv) == 1 else sys.argv[1])

    @classmethod
    def _ignoreAttributes(cls):
        return [
            "initConfig",
            "readConfigFile",
            "storeConfigInFile",
            "getConfigValues",
            "logConfigValues"
        ]

    @classmethod
    def getConfigValues(cls):
        configValues = {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
        for attribute in cls._ignoreAttributes():
            configValues.pop(attribute, None)
        return configValues

    @classmethod
    def logConfigValues(cls):
        cls._log.debug("Config values:\n{}".format(json.dumps(cls.getConfigValues(),  indent=4)))

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

    @classmethod
    def initConfig(cls):
        raise NotImplementedError()
