import os
import json
import logging
import sys

import utils


class ConfigException(Exception):
    pass


class ConfigBase:
    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._configFilePath = utils.PROGRAM_PATH + os.sep + ("config.json" if len(sys.argv) == 1 else sys.argv[1])

    def _ignoreAttributes(self):
        return [
            "initConfig",
            "readConfigFile",
            "storeConfigInFile",
            "getConfigValues",
            "logConfigValues"
        ]

    def getConfigValues(self):
        configValues = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        for attribute in self._ignoreAttributes():
            configValues.pop(attribute, None)
        return configValues

    def logConfigValues(self):
        self._log.debug("Config values:\n{}".format(json.dumps(self.getConfigValues(), indent=4)))

    def readConfigFile(self):
        if os.path.exists(self._configFilePath):
            try:
                self._log.info("Reading config file")
                with open(self._configFilePath) as f:
                    jsonObject = json.load(f)
                self.__dict__.update(jsonObject)
            except ValueError:
                self._log.error("Json corrupted so it was ignored, necessary to check!")
        else:
            self.storeConfigInFile()

    def storeConfigInFile(self):
        with open(self._configFilePath, "w") as f:
            configValues = self.getConfigValues()
            json.dump(configValues, f, indent=4)

    def initConfig(self):
        raise NotImplementedError()
