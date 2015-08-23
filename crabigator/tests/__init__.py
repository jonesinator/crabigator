import os
import sys
import unittest

def main():
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite(unittest.TestLoader().loadTestsFromNames([
                               'crabigator.tests.test_wanikani']))
    raise SystemExit(not runner.run(suite).wasSuccessful())

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()
