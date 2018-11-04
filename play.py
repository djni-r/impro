import multiprocessing as mp
from argparse import ArgumentParser
from threading import Thread
from contextlib import closing
import impro
from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer


def play(instrument = "piano", key = None, mode = None,
         beat = (4,4), bpm = 60, max_mem = None,
         max_octave = 5, max_tone = 12, min_octave = 1, min_tone = 1):

    try:
        mind = Mind(instrument, key, mode, beat, bpm,
                    max_mem, max_octave, max_tone,
                    min_octave, min_tone)
        
        if instrument == "cello":
            unit_player = CelloUnitPlayer(bpm)
            mind.min_octave = 2
            mind.max_octave = 3
        elif instrument == "xylo":
            unit_player = XyloUnitPlayer(bpm)
            mind.min_octave = 4
            mind.min_tone = 10
            mind.max_octave = 7
            mind.max_tone = 7
        else:
            unit_player = UnitPlayer(bpm)
    
            mind.start_beat()

        while True:
            unit = mind.choose_unit()
            unit.play(unit_player)
    except (KeyboardInterrupt):
        print "\nStopping {}".format(instrument)
        

    
if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("instrument", choices=["piano","cello","xylo"],
                           nargs="+")
    args = argparser.parse_args()

    try:
        with closing(mp.Pool(len(args.instrument))) as pool:
            pool.map(play, args.instrument)
    except (KeyboardInterrupt):
        print "Exiting"

    
        

    
        
    
    

        
        
        


        
