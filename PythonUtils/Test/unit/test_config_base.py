import json
import logging
import unittest

from flexmock import flexmock, flexmock_teardown

from config_base import ConfigBase
from Test.pythonTestUtils.TestUtils import *


class TestConfigBase(unittest.TestCase):
    def setUp(self):
        ConfigBase.init_config = lambda x: None
        self.configBase = ConfigBase()
        self.configBase._config_file_path = os.path.join(getTemporaryTestFilesPath(), "c-test.json")
        self.configBase.__dict__.update(dict(ep1=1, ep2=2, ep3="3"))

    def tearDown(self):
        flexmock_teardown()
        cleanTemporaryTestFiles()

    def test_readConfigFile_changesConfigParameters(self):
        self.configBase._config_file_path = os.path.join(getTestResourcesPath(), "c-test.json")
        self.configBase.read_config_file()

        self.assertEqual(self.configBase.ep1, 11)
        self.assertEqual(self.configBase.ep2, 22)

    def test_readConfigFile_cachesErrorIfCorruptedFile(self):
        self.configBase._config_file_path = os.path.join(getTestResourcesPath(), "corrupted-config.json")
        self.configBase._log = flexmock(logging.getLogger(__name__))
        self.configBase._log.should_receive("error").once()

        try:
            self.configBase.read_config_file()
        except:
            self.fail("Exception not cached")


    def test_readConfigFile_ConfigNotChangedIfCorruptedFile(self):
        self.configBase._config_file_path = os.path.join(getTestResourcesPath(), "corrupted-config.json")
        originalConfigDict = self.configBase.get_config_values()
        self.configBase.read_config_file()

        for k, v in self.configBase.get_config_values().items():
            self.assertEqual(originalConfigDict[k], v)

    def test_storeConfigInFile_createsNewFileIfNotExists(self):
        self.assertFalse(os.path.exists(self.configBase._config_file_path), "assert file does not exist")

        self.configBase.store_config_in_file()

        self.assertTrue(os.path.exists(self.configBase._config_file_path))

    def test_storeConfigInFile_overWriteFileIfExist(self):
        with open(self.configBase._config_file_path, "w") as f:
            f.write("Testing")

        self.configBase.store_config_in_file()

        with open(self.configBase._config_file_path) as f:
            self.assertNotEqual(f.read(), "Testing")

    def test_storeConfigInFile_createsAJsonWithAllConfigValues(self):
        self.configBase.store_config_in_file()
        with open(self.configBase._config_file_path) as f:
            obj = json.load(f)

        for k, v in self.configBase.get_config_values().items():
            self.assertEqual(obj[k], v)
