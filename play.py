from argparse import ArgumentParser
from multiprocessing import Pool
from contextlib import closing

from tkinter import *
from tkinter import ttk

from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer

class App(object):
    def __init__(self):
        self.play = True

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
            while self.play:
                unit = mind.choose_unit()
                unit.play(unit_player)

    def stop(self):
        self.play = False
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"],
                           nargs="+", default="piano")
    args = argparser.parse_args()

    app = App()
    root = Tk()
    root.title("Impro")
    mainframe = ttk.Frame(root, padding="3")
    mainframe.grid(column=0, row=0, sticky=(N,W,S,E))
    piano_btn = ttk.Button(mainframe, text = "Piano", command=app.play)
    piano_btn.grid(column=2, row=2, sticky=(W,E))
    root.mainloop()
#    with closing(Pool(max_instr)) as pool:
#        pool.map(play, args.instrument)
        
        
        


        
