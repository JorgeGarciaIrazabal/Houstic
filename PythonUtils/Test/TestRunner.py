import os
import unittest
import sys
import xmlrunner

sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "PythonUtils")]

from unit.testConfigBase import TestConfigBase


def __runTests(suite):
    1/0
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(suite)


def runUnitTests():

    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestConfigBase))
    __runTests(suite)

if __name__ == '__main__':
    runUnitTests()