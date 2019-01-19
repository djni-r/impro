import random
import logging
import time
import os
import math
from threading import Thread
from playsound import playsound
from argparse import ArgumentParser
from collections import OrderedDict
from tkinter import *
from tkinter import ttk

import vendor.load_sounds as load_sounds
from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer, CelloUnitPlayer, XyloUnitPlayer

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
LOGGER = logging.getLogger()


class App(object):

    WINDOW_WIDTH = 1411
    WINDOW_HEIGHT = 794
    PROCESSES = 10
    INSTRUMENTS = ('piano', 'cello', 'xylo')
                   
    def __init__(self, track):
        self.stop_dict = dict( zip(App.INSTRUMENTS,
                                  ( False for i in range(len(App.INSTRUMENTS)) )) )
        self.root = Tk()
        self.root.title("Impro") 
        self.mainframe = ttk.Frame(self.root, padding="3")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,S,E))
        self.mainframe.bind('<Destroy>', lambda e: self.stop_all())
        self.btn_dict = OrderedDict()

        for i, instr in enumerate(App.INSTRUMENTS):
            btn = ttk.Button(
                self.mainframe,
                text = instr.capitalize(),
                command = self.start_command(instr))
            btn.grid(column=0, row=i, stick=(W,E))
            self.btn_dict[instr] = btn
            
        sound_paths = load_sounds.misc(track)
        commands = [lambda i=i: Thread(target=self.play_sound,
                                       args=(sound_paths[i],)).start() \
                    for i in range(len(sound_paths))]
        rows = int(math.ceil( math.sqrt(len(commands)) ))
        
        for e,c in enumerate(commands):
            LOGGER.debug((e,c))
            btn = ttk.Button(
                self.mainframe,
                text = os.path.basename(sound_paths[e]).split('.')[0],
                command = c)
            btn.grid(column=e/rows+1, row=e % rows, stick=(W,E))
            self.btn_dict['sound'+str(e+1)] = btn
            
        LOGGER.debug("ending init")

        
    def play(self, instrument = "piano", key = None, mode = None,
             beat = (4,4), bpm = 60, max_mem = None,
             max_octave = 5, max_tone = 12, min_octave = 1, min_tone = 1):

        self.stop_dict[instrument] = False

        LOGGER.debug('in play ' + instrument)

        mind = Mind(instrument, key, mode, beat, bpm,
                    max_mem, max_octave, max_tone,
                    min_octave, min_tone)

        #NOTE! should make a unitPlayer factory to put here
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

        self.btn_dict[instrument]['command'] = lambda: self.stop(instrument)
        #! doesn't work yet    
        mind.start_beat()
        
        while not self.stop_dict[instrument]:
            unit = mind.choose_unit()
            unit.play(unit_player)

        self.stop_flag = False

        
    def start_command(self, instr):
        return lambda: Thread(target=self.play, args=(instr,)).start()

    
    def stop(self, instr):
        self.stop_dict[instr] = True
        self.btn_dict[instr]['command'] = self.start_command(instr)


    def stop_all(self):
        for key in self.stop_dict:
            self.stop_dict[key] = True
            
        
    def play_sound(self, sound):
        LOGGER.debug(sound)
        playsound(sound, False)
        
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    dirname = "vendor/resources/misc_sounds"
    argparser.add_argument("track",
                           choices = [ str(i) for i in range(1, len(
                               os.listdir(dirname))+1) ], nargs=1)
                               
                               
    args = argparser.parse_args()
    app = App(args.track[0])
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        LOGGER.error("exiting")
        
        


        
