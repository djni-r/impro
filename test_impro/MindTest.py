import unittest

from impro.Mind import Mind
from impro.Sequence import Sequence
from impro.unit import Note, Pattern

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

    #@unittest.skip("ok")
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
                                     Note("B", 4, "1/4"))

        result = []
        for i in range(7):
            unit = self.mind.choose_unit()
            result.append(unit)

        print(list(str(n) for n in result))
        self.assertEqual(result, self.c_scale[::-1])


        
    def test_choose_unit_pattern(self):
        pc = self.mind.prob_calc
        pc.pattern_prob = lambda: 1
        pc.pat_form_probs = lambda: [0,1,0,0,0,0,0]
        pc.pat_mode_probs = lambda: [1,0]
        pc.seq_prob = lambda: 1

        self.mind.cur_seq = Sequence("scale", 7, "C", "major", 1,
                                     Pattern("terza", "major",
                                             [self.c_scale[0], self.c_scale[2]])
        )
        self.mind.cur_seq.cur_pos += 1
        unit = self.mind.choose_unit()
        print unit
        
        expected = Pattern("terza", "major", [Note("D",4,"1/4"),Note("Gb",4,"1/4")])
        self.assertEqual(expected, unit)


    def test_choose_unit_pattern_seq_back(self):
        first_pat = Pattern([Note("F", 5, "1/12")], "sexta", "major")
        
        self.mind.cur_seq = Sequence("triad", 5, "A", "major", -1, first_pat)
                                    
        result = [first_pat]
        for i in range(4):
            unit = self.mind.choose_unit()
            print(unit.key)
            result.append(unit)
            
        print(list(str(n) for n in result))

        
    def test_choose_unit_pattern_max(self):
        pc = self.mind.prob_calc
        pc.pattern_prob = lambda: 1
        pc.pat_form_probs = lambda: [0,0,0,0,0,1,0]
        pc.pat_mode_probs = lambda: [0,1]
        pc.seq_prob = lambda: 1

        self.mind.cur_seq = Sequence("scale", 7, "C", "major", 1,
                                     Pattern("septima", "minor",
                                             [Note("C",5,"1/4"), Note("B",5,"1/4")]
                                     )
        )
        self.mind.cur_seq.cur_pos += 1
        unit = self.mind.choose_unit()
        print unit

        expected = Pattern("septima", "minor", [Note("D",5,"1/4")])
        self.assertEqual(expected, unit)
        
#if __name__ == '__main__':
#    unittest.main(verbosity = 2)
