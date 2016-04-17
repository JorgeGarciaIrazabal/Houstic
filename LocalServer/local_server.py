import sys
import os

sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, "PythonUtils")]

import json
import logging.config

import utils
from libs.Config import Config
from libs.House import House

os.chdir(utils.get_module_path())

logging.config.dictConfig(json.load(open('logging.json')))

if __name__ == '__main__':
    Config.get().init_config()
    House().initialize_communications()
