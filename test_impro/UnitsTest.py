import unittest

from impro.unit import Pattern, Note


class UnitsTest(unittest.TestCase):

    def test_pattern_setters(self):
        pattern = Pattern("terza", "minor", Note("C", 4, "1/4"))
        print(pattern.base_unit)
        
        pattern.pitch = "D"
        pattern.octave = 5
        print(pattern.base_unit)
        
        self.assertEqual(pattern.base_unit, Note("D", 5, "1/4"))
