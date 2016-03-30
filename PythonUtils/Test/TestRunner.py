import unittest
import xmlrunner

def __runTests(suite):
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(suite)


def runUnitTests():
    from Test.unit.testConfigBase import TestConfigBase

    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestConfigBase))
    __runTests(suite)

if __name__ == '__main__':
    runUnitTests()