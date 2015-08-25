"""Runs unit tests for the crabigator module."""

import os
import sys
import unittest


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))
    RUNNER = unittest.TextTestRunner()
    SUITE = unittest.TestSuite(unittest.TestLoader().loadTestsFromNames([
        'crabigator.tests.test_wanikani']))
    raise SystemExit(not RUNNER.run(SUITE).wasSuccessful())
