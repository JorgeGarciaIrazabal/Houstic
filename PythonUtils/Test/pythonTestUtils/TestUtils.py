import os
import shutil

import utils


def getTestResourcesPath():
    return os.path.join(utils.getModulePath(), os.pardir, "resources")

def getTemporaryTestFilesPath(constructFolderStructure = True):
    path = os.path.join(utils.getModulePath(), os.pardir, "tempTestFiles")
    if constructFolderStructure and not os.path.exists(path):
        os.makedirs(path)
    return path

def cleanTemporaryTestFiles():
    tempPath = getTemporaryTestFilesPath(False)
    if os.path.exists(tempPath):
        shutil.rmtree(getTemporaryTestFilesPath(False))