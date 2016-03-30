import sys
import os

sys.path += [os.path.join(__file__, os.pardir, "PythonUtils")]

import json
import logging.config

import utils
from libs.Config import Config
from libs.House import House

os.chdir(utils.getModulePath())

logging.config.dictConfig(json.load(open('logging.json')))


if __name__ == '__main__':
    Config.initConfig()
    House().initializeCommunications()


