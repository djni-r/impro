import unittest
import sys
from test_impro.UnitsTest import UnitsTest
from test_impro.MindTest import MindTest
from test_impro.GraphicUnitPlayerTest import GraphicUnitPlayerTest


suite = unittest.TestLoader().loadTestsFromTestCase(GraphicUnitPlayerTest)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
