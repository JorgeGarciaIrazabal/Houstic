import json
import logging
import logging.config

from libs.Config import Config
from libs.House import House

logging.config.dictConfig(json.load(open('logging.json')))

if __name__ == '__main__':
    Config.readConfigFile()
    House().initializeCommunications()


