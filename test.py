import unittest
import doctest
import json2line

suite = doctest.DocTestSuite(json2line)
runner = unittest.TextTestRunner()
runner.run(suite)

