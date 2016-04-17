import glob
import inspect
import os
from os.path import join
import unittest
import sys
import xmlrunner

def get_module_path():
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    file_name = info.filename
    return os.path.dirname(os.path.abspath(file_name))

sys.path += [os.path.join(get_module_path(), "PythonUtils")]
print sys.path[-1]

def __get_suites():
    path = get_module_path()
    test_files = glob.glob(join(path, "PythonUtils", "Test", "unit", 'test*.py'))
    relative_test_files = [test_file.split(os.sep)[-3:] for test_file in test_files]
    module_strings = [".".join(test_file)[:-3] for test_file in relative_test_files]
    print module_strings
    for t in module_strings:
        try:
            unittest.defaultTestLoader.loadTestsFromName(t)
            print t, 'good'
        except Exception as e:
            print t, str(e)
    return [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]


def __runTests(suite):
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(suite)


def runUnitTests():
    suite = unittest.TestSuite(__get_suites())
    __runTests(suite)

if __name__ == '__main__':
    runUnitTests()