import glob2
import importlib
import os


def importAllHubs():
    allHubs = glob2.glob("Hubs/*Hub.py")
    allModules = map(lambda x: x.split(os.sep)[1].split(".")[0], allHubs)
    for module in allModules:
        importlib.import_module("Hubs." + module)