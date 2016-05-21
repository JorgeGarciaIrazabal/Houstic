import os
import json
import logging
import sys

import utils


class ConfigException(Exception):
    pass


class ConfigBase(object):
    __instance = None

    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._config_file_path = ("config.json" if len(sys.argv) == 1 else sys.argv[1])
        self.init_config()

    def _ignore_attributes(self):
        return [
            "init_config",
            "read_config_file",
            "store_config_in_file",
            "get_config_values",
            "log_config_values"
        ]

    def get_config_values(self):
        config_values = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        for attribute in self._ignore_attributes():
            config_values.pop(attribute, None)
        return config_values

    def log_config_values(self):
        self._log.debug("Config values:\n{}".format(json.dumps(self.get_config_values(), indent=4)))

    def read_config_file(self):
        if os.path.exists(self._config_file_path):
            try:
                self._log.info("Reading config file")
                with open(self._config_file_path) as f:
                    json_object = json.load(f)
                self.__dict__.update(json_object)
            except ValueError:
                self._log.error("Json corrupted so it was ignored, necessary to check!")
                return  # we don't want to overwrite corrupted files in order to not lose all configuration
        self.store_config_in_file()

    def store_config_in_file(self):
        with open(self._config_file_path, "w") as f:
            config_values = self.get_config_values()
            json.dump(config_values, f, indent=4)

    def init_config(self):
        raise NotImplementedError()

    @classmethod
    def get(cls):
        """
        :rtype: ConfigBase
        """
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
