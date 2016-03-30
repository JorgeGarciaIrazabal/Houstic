import sys
import os
sys.path += [os.path.join(__file__, os.pardir, "PythonUtils")]

import json
import logging.config

from libs.Config import Config
from libs.House import House

logging.config.dictConfig(json.load(open('logging.json')))


if __name__ == '__main__':
    Config.initConfig()
    House().initializeCommunications()


