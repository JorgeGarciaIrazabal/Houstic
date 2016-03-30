import json
import logging
import unittest

from flexmock import flexmock, flexmock_teardown

from ConfigBase import ConfigBase
from Test.pythonTestUtils.TestUtils import *


class TestConfigBase(unittest.TestCase):
    def setUp(self):
        ConfigBase.initConfig = lambda x: None
        self.configBase = ConfigBase()
        self.configBase._configFilePath = os.path.join(getTemporaryTestFilesPath(), "c-test.json")
        self.configBase.__dict__.update(dict(ep1=1, ep2=2, ep3="3"))

    def tearDown(self):
        flexmock_teardown()
        cleanTemporaryTestFiles()

    def test_readConfigFile_changesConfigParameters(self):
        self.configBase._configFilePath = os.path.join(getTestResourcesPath(), "c-test.json")
        self.configBase.readConfigFile()

        self.assertEqual(self.configBase.ep1, 11)
        self.assertEqual(self.configBase.ep2, 22)

    def test_readConfigFile_cachesErrorIfCorruptedFile(self):
        self.configBase._configFilePath = os.path.join(getTestResourcesPath(), "corrupted-config.json")
        self.configBase._log = flexmock(logging.getLogger(__name__))
        self.configBase._log.should_receive("error").once()

        try:
            self.configBase.readConfigFile()
        except:
            self.fail("Exception not cached")


    def test_readConfigFile_ConfigNotChangedIfCorruptedFile(self):
        self.configBase._configFilePath = os.path.join(getTestResourcesPath(), "corrupted-config.json")
        originalConfigDict = self.configBase.getConfigValues()
        self.configBase.readConfigFile()

        for k, v in self.configBase.getConfigValues().items():
            self.assertEqual(originalConfigDict[k], v)

    def test_storeConfigInFile_createsNewFileIfNotExists(self):
        self.assertFalse(os.path.exists(self.configBase._configFilePath), "assert file does not exist")

        self.configBase.storeConfigInFile()

        self.assertTrue(os.path.exists(self.configBase._configFilePath))

    def test_storeConfigInFile_overWriteFileIfExist(self):
        with open(self.configBase._configFilePath, "w") as f:
            f.write("Testing")

        self.configBase.storeConfigInFile()

        with open(self.configBase._configFilePath) as f:
            self.assertNotEqual(f.read(), "Testing")

    def test_storeConfigInFile_createsAJsonWithAllConfigValues(self):
        self.configBase.storeConfigInFile()
        with open(self.configBase._configFilePath) as f:
            obj = json.load(f)

        for k, v in self.configBase.getConfigValues().items():
            self.assertEqual(obj[k], v)
