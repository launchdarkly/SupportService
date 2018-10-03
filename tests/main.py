import os
import sys
import unittest
import xmlrunner

if __name__ == '__main__':
    root_dir = os.path.dirname(__file__)
    test_loader = unittest.TestLoader()
    package_tests = test_loader.discover(start_dir=root_dir)

    testRunner = xmlrunner.XMLTestRunner(output='test-reports')
    results = testRunner.run(package_tests)

    if (len(results.failures) > 0 or len(results.errors) > 0):
        sys.exit(1)