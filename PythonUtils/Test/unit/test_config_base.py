import json
import logging
import unittest
from flexmock import flexmock, flexmock_teardown
from config_base import ConfigBase
from Test.python_test_utils.test_utils import *


class TestConfigBase(unittest.TestCase):
    def setUp(self):
        ConfigBase.init_config = lambda x: None
        self.configBase = ConfigBase()
        self.configBase._config_file_path = os.path.join(get_temporary_test_files_path(), "c-test.json")
        self.configBase.__dict__.update(dict(ep1=1, ep2=2, ep3="3"))

    def tearDown(self):
        flexmock_teardown()
        clean_temporary_test_files()

    def test_readConfigFile_changesConfigParameters(self):
        self.configBase._config_file_path = os.path.join(get_test_resources_path(), "c-test.json")
        self.configBase.read_config_file()

        self.assertEqual(self.configBase.ep1, 11)
        self.assertEqual(self.configBase.ep2, 22)

    def test_readConfigFile_cachesErrorIfCorruptedFile(self):
        self.configBase._config_file_path = os.path.join(get_test_resources_path(), "corrupted-config.json")
        self.configBase._log = flexmock(logging.getLogger(__name__))
        self.configBase._log.should_receive("error").once()

        try:
            self.configBase.read_config_file()
        except:
            self.fail("Exception not cached")

    def test_readConfigFile_ConfigNotChangedIfCorruptedFile(self):
        self.configBase._config_file_path = os.path.join(get_test_resources_path(), "corrupted-config.json")
        original_config_dict = self.configBase.get_config_values()
        self.configBase.read_config_file()

        for k, v in self.configBase.get_config_values().items():
            self.assertEqual(original_config_dict[k], v)

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
