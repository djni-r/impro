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
        "-" : ("white",),
        "C" : ("#FF0000", "#EF0000", "#DF0000", "#CF0000", "#BF0000", "#AF0000"), #red
        "Db": ("#FF6100", "#F85900", "#EF5100", "#E84800", "#DF4100", "#D83900"), #red-orange
        "D" : ("#FFA500", "#F79D00", "#EF9500"),#orange
        "Eb": ("#FFAD00", "#FFB400", "#FFBD00"), #yellow-orange
        "E" : ("#FFFF00", "#F7F700", "#EFEF00", "#DFDF00"), #yellow
        "F" : ("#00FF00", "#00EE00", "#00DD00", "#00CC00", "#00BB00", "#00AA00"), #green
        "Gb": ("#00FFFF", "#00DDDD", "#00BBBB", "#009999"), #green-blue
        "G" : ("#0000FF", "#0000DD", "#0000BB", "#0000AA", "#000099"), #blue
        "Ab": ("#000088", "#000077", "#000066",), #blue-darkblue
        "A" : ("#000055", "#00004D", "#000045", "#00003D", "#000035"),
        "Bb": ("#8000ff", "#8000ee", "#8000cc", "#8000aa", "#800099"),  #darkblue-purple
        "B" : ("#800080", "#780078", "#700070", "#680068", "#600060", "#500050") #purple
    }
    keys = ["-", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    WINDOW_WIDTH = 1411
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
                                 fill = random.choice(App.note_color[u_key]), outline = 'white', width = 2)


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

        
        
        


        
