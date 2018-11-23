import unittest
from vendor.GraphicUnitPlayer import GraphicUnitPlayer
from impro.unit import Note

class GraphicUnitPlayerTest(unittest.TestCase):

    def test_play_note(self):
        keys = ["C","D","E","F","G","A","B"]
        player = GraphicUnitPlayer()

        for key in keys:
            Note(key, 4, 1/4).play(player)
        
