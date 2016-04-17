import os
import shutil

import utils


def get_test_resources_path():
    return os.path.join(utils.get_module_path(), os.pardir, "resources")


def get_temporary_test_files_path(construct_folder_structure=True):
    path = os.path.join(utils.get_module_path(), os.pardir, "tempTestFiles")
    if construct_folder_structure and not os.path.exists(path):
        os.makedirs(path)
    return path


def clean_temporary_test_files():
    temp_path = get_temporary_test_files_path(False)
    if os.path.exists(temp_path):
        shutil.rmtree(get_temporary_test_files_path(False))
