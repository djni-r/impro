import random

from argparse import ArgumentParser
from multiprocessing import Pool
from contextlib import closing

from tkinter import *
from tkinter import ttk

from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer

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

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 450
                   
    def __init__(self):
        self.stop_flag = False
        
        self.master = Tk()
        self.master.title("Impro")
        self.cs = Canvas(self.master, width = App.WINDOW_WIDTH,
                         height = App.WINDOW_HEIGHT)
        #piano_btn = ttk.Button(self.master, text = "Piano", command=self.play)
        self.cs.pack()
        #self.master.update()
        print("end app init")
        

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
                #for u in unit.units:
                self.cs.create_rectangle(random.randrange(App.WINDOW_WIDTH), random.randrange(App.WINDOW_HEIGHT), random.randrange(App.WINDOW_WIDTH), random.randrange(App.WINDOW_HEIGHT), fill = App.note_color[unit.key], outline = 'white', width = 3)
                print("created")
                self.master.update()
                unit.play(unit_player)

    def stop(self):
        self.stop_flag = True
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"],
                           nargs="+", default="piano")
    args = argparser.parse_args()

    app = App()
            
    #mainframe = ttk.Frame(root, padding="3")
    #mainframe.grid(column=0, row=0, sticky=(N,W,S,E))
    #
    #piano_btn.grid(column=2, row=2, sticky=(W,E))

    app.play(args.instrument[0])
#    with closing(Pool(max_instr)) as pool:
#        pool.map(app.play, args.instrument)
        
        
        


        
