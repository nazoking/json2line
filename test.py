import unittest
import doctest
import sys
import json2line

suite = doctest.DocTestSuite(json2line)
runner = unittest.TextTestRunner()
runner.run(suite)
