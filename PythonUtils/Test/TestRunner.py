import os
import unittest
import sys
import xmlrunner

from unit.testConfigBase import TestConfigBase

sys.path += [os.path.join(os.path.dirname(__file__), os.pardir, "PythonUtils")]

def __runTests(suite):
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(suite)


def runUnitTests():

    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestConfigBase))
    __runTests(suite)

if __name__ == '__main__':
    runUnitTests()