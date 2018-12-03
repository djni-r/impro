import random
import logging

from argparse import ArgumentParser
from multiprocessing import Pool
from contextlib import closing

from Tkinter import *

from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer


logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger()

class App(object):
    note_color = {
        "-" : "white",
        "A" : "red",
        "B" : "orange",
        "C" : "yellow",
        "D" : "green",
        "E" : "blue",
        "F" : "darkblue",
        "G" : "purple",
        "Ab": "#AD0080",
        "Bb": "#FF5100",
        "Db": "#BDFF00",
        "Eb": "#0087FF",
        "Gb": "#51008B"
    }

    WINDOW_WIDTH = 794
    WINDOW_HEIGHT = 794
                   
    def __init__(self):
        self.stop_flag = False
        
        self.master = Tk()
        self.master.title("Impro")
        self.cs = Canvas(self.master, width = App.WINDOW_WIDTH,
                         height = App.WINDOW_HEIGHT)
   
        self.cs.pack()
        logger.info("end app init")
        

    def play(self, instrument = "piano", key = None, mode = None,
             beat = (4,4), bpm = 60, max_mem = None,
             max_octave = 5, max_tone = 12, min_octave = 1, min_tone = 1):
        print("play " + instrument)
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
            
        while not self.stop_flag:
            unit = mind.choose_unit()
            for u in unit.units:
                self.cs.create_rectangle(random.randrange(App.WINDOW_WIDTH), random.randrange(App.WINDOW_HEIGHT), random.randrange(App.WINDOW_WIDTH), random.randrange(App.WINDOW_HEIGHT), fill = App.note_color[u.key], outline = 'white', width = 3)
                self.master.update()
                u.play(unit_player)

    def stop(self):
        self.stop_flag = True
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"], nargs=1)
    args = argparser.parse_args()

    app = App()
    app.play(args.instrument[0])

        
        
        


        
