import unittest
from test_impro.MindTest import MindTest


suite = unittest.TestLoader().loadTestsFromTestCase(MindTest)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
