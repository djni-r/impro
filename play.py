from argparse import ArgumentParser

from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer


def play(instrument = "piano", key = None, mode = None,
         beat = (4,4), bpm = 60, max_mem = None,
         max_octave = 5, min_octave = 1):
    
    mind = Mind(instrument, key, mode, beat, bpm,
                max_mem, max_octave, min_octave)
    
    if instrument == "cello":
        unit_player = CelloUnitPlayer(bpm)
        mind.min_octave = 2
        mind.max_octave = 3
    else:
        unit_player = UnitPlayer(bpm)
    
    mind.start_beat()
    while True:
        unit = mind.choose_unit()
        unit.play(unit_player)

        
if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("instrument", choices=["piano","cello"],
                           nargs="?", default="piano")
    args = argparser.parse_args()
    play(args.instrument)


        
