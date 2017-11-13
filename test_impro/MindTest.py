import unittest

from impro.Mind import Mind
from impro.Sequence import Sequence
from impro.unit import Note

class MindTest(unittest.TestCase):

    def setUp(self):
        self.mind = Mind()
        self.c_scale = [
            Note("C", 4, "1/4"),
            Note("D", 4, "1/4"),
            Note("E", 4, "1/4"),
            Note("F", 4, "1/4"),
            Note("G", 4, "1/4"),
            Note("A", 4, "1/4"),
            Note("B", 4, "1/4")
        ]

    @unittest.skip("ok")
    def test_choose_unit_with_seq(self):
        self.mind.cur_seq = Sequence("scale", 7, "C", "major", 1,
                                     Note("C", 4, "1/4"))
        
        result = []
        for i in range(7):
            unit = self.mind.choose_unit()
            result.append(unit)
            
        print(list(str(n) for n in result))
        self.assertEqual(result, self.c_scale)


    def test_choose_unit_seq_backwards(self):
        self.mind.cur_seq = Sequence("scale", 7, "C", "major", -1,
                                     Note("B", 4, 1/4))

        result = []
        for i in range(7):
            unit = self.mind.choose_unit()
            result.append(unit)

        print(list(str(n) for n in result))
        self.assertEqual(result, self.c_scale[::-1])
        
#if __name__ == '__main__':
#    unittest.main(verbosity = 2)
