import unittest
from test_impro.UnitsTest import UnitsTest


suite = unittest.TestLoader().loadTestsFromTestCase(UnitsTest)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
