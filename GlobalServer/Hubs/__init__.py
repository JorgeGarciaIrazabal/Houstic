import glob2
import importlib
import os


def import_all_hubs():
    all_hubs = glob2.glob("hubs/*_hub.py")
    all_modules = map(lambda x: x.split(os.sep)[1].split(".")[0], all_hubs)
    for module in all_modules:
        importlib.import_module("hubs." + module)