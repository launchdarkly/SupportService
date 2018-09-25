import os
import unittest
import xmlrunner

if __name__ == '__main__':
    root_dir = os.path.dirname(__file__)
    test_loader = unittest.TestLoader()
    package_tests = test_loader.discover(start_dir=root_dir)

    testRunner = xmlrunner.XMLTestRunner(output='test-reports')
    testRunner.run(package_tests)