import json
import logging
import os
import sys

import utils
from ConfigBase import ConfigBase


class ConfigException(Exception):
    pass


class Config(ConfigBase):
    port = 9517
    mongo = dict(db="houstic", host=None, port=None, username=None, password=None)
    JSClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "Application", "HousticApp", "app", "libs")
    PyClientPath = os.path.join(utils.PROGRAM_PATH, os.pardir, "LocalServer", "libs")

    @classmethod
    def initConfig(cls):
        cls.readConfigFile()
        cls.logConfigValues()
