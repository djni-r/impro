import random
import logging

from fractions import Fraction
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
        "C" : "red",
        "Db": "#FF5100", #red-orange
        "D" : "orange",
        "Eb": "#9ACD32", #yellow-green
        "E" : "yellow",
        "F" : "green",
        "Gb": "#0087FF", #green-blue
        "G" : "blue",
        "Ab": "#0000C1", #blue-darkblue
        "A" : "darkblue",
        "Bb": "#51008B",  #darkblue-purple
        "B" : "purple"
    }
    keys = ["-", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

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
               # self.random_rect(u.key)
                logger.debug(u.key)
                logger.debug(u.octave)
                self.placed_rect(u.key, u.octave, u.duration,
                                 mind.min_octave, mind.max_octave)
                
                self.master.update()
                u.play(unit_player)


    def placed_rect(self, u_key, u_octave, u_dur, min_octave, max_octave):
        seg_height = App.WINDOW_HEIGHT / (max_octave - min_octave + 1)
        subseg_height = seg_height / 13
        rand = random.randrange(App.WINDOW_WIDTH)
        seg_width = App.WINDOW_WIDTH / (u_octave - min_octave + 1 if u_octave != 0 else 1)
        subseg_width = seg_width / 13
        self.cs.create_rectangle(rand,
                                 random.randrange(App.WINDOW_HEIGHT - seg_height * (u_octave - min_octave) - subseg_height * (App.keys.index(u_key) + 1), App.WINDOW_HEIGHT - seg_height * (u_octave - min_octave) - subseg_height * (App.keys.index(u_key))),
                                 rand + App.WINDOW_WIDTH * Fraction(u_dur) / 2.0,
                                 random.randrange(App.WINDOW_HEIGHT - seg_height * (u_octave - min_octave) - subseg_height * (App.keys.index(u_key) + 1), App.WINDOW_HEIGHT - seg_height * (u_octave - min_octave) - subseg_height * (App.keys.index(u_key))) + seg_width / (u_octave if u_octave !=0 else 1) / 3,
                                 fill = App.note_color[u_key], outline = 'white', width = 1)


    def random_rect(self, u_key):
        self.cs.create_rectangle(random.randrange(App.WINDOW_WIDTH),
                                 random.randrange(App.WINDOW_HEIGHT),
                                 random.randrange(App.WINDOW_WIDTH),
                                 random.randrange(App.WINDOW_HEIGHT),
                                 fill = App.note_color[u_key], outline = 'white', width = 3)

        
    def stop(self):
        self.stop_flag = True
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"], nargs=1)
    args = argparser.parse_args()

    app = App()
    app.play(args.instrument[0])

        
        
        


        
