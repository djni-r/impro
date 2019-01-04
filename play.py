import random
import logging
import time
from threading import Thread
from playsound import playsound
from fractions import Fraction
from argparse import ArgumentParser
from multiprocessing import Pool, Queue, Process
from contextlib import closing
from tkinter import *
from tkinter import ttk

import vendor.load_sounds as load_sounds
from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger()


class App(object):

    WINDOW_WIDTH = 1411
    WINDOW_HEIGHT = 794
    PROCESSES = 10
    SOUND1_PATH = 'vendor/resources/misc_sounds/001.wav'
    SOUND2_PATH = 'vendor/resources/misc_sounds/002.wav'
                   
    def __init__(self):
        self.stop_flag = False
        
        self.root = Tk()
        self.root.title("Impro")

        
        self.pool = Pool(App.PROCESSES)

        logger.debug("after process loop")

        self.mainframe = ttk.Frame(self.root, padding="3")
        self.mainframe.grid(column=2, row=3, sticky=(N,W,S,E))
        self.piano_btn = ttk.Button(self.mainframe, text = "Piano", command = lambda:
                                    Thread(target=self.play, args=('piano',self.piano_btn)).start())
        self.cello_btn = ttk.Button(self.mainframe, text = "Cello", command = lambda:
                                    Thread(target=self.play, args=('cello',)).start())
        self.xylo_btn = ttk.Button(self.mainframe, text = "Xylo", command = lambda:
                                    Thread(target=self.play, args=('xylo',)).start())
        self.s1_btn = ttk.Button(self.mainframe, text = "Sound 1",
                            command = lambda : self.play_sound(App.SOUND1_PATH))
        self.s2_btn = ttk.Button(self.mainframe, text = "Sound 2",
                            command = lambda : self.play_sound(App.SOUND2_PATH))
                            
        self.piano_btn.grid(column=1, row=1, sticky=(W,E))
        self.cello_btn.grid(column=1, row=2, sticky=(W,E))
        self.xylo_btn.grid(column=1, row=3, sticky=(W,E))
        self.s1_btn.grid(column=2, row=1, sticky=(W,E))
        self.s2_btn.grid(column=2, row=2, sticky=(W,E))

        logger.debug("ending init")
   

        

    def play(self, instrument = "piano", key = None, mode = None,
             beat = (4,4), bpm = 60, max_mem = None,
             max_octave = 5, max_tone = 12, min_octave = 1, min_tone = 1):

        logger.debug('in play ' + instrument)
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
            unit.play(unit_player)


    def play_sound(self, sound, btn):
        playsound(sound, False)
        
                              
    def stop(self):
        logger.debug('stopping')
        self.stop_flag = True
        
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"], nargs=1)
    args = argparser.parse_args()
    app = App()
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        logger.error("exiting")
        
        


        
