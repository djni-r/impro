import random
import logging
import time
import os
from threading import Thread
from playsound import playsound
from fractions import Fraction
from argparse import ArgumentParser
from multiprocessing import Pool, Queue, Process
from collections import OrderedDict
from contextlib import closing
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
    SOUND_PATH = "vendor/resources/misc_sounds/00{}.wav"
                   
    def __init__(self):
        self.stop_dict = { 'piano' : False, 'cello' : False, 'xylo' : False }
        
        self.root = Tk()
        self.root.title("Impro")

        
        self.pool = Pool(App.PROCESSES)

        LOGGER.debug("after process loop")

        self.mainframe = ttk.Frame(self.root, padding="3")
        self.mainframe.grid(column=3, row=3, sticky=(N,W,S,E))

        self.btn_dict = OrderedDict()
        
        self.btn_dict['piano'] = ttk.Button(
            self.mainframe,
            text = "Piano",
            command = self.start_command('piano'))
        
        self.btn_dict['cello'] = ttk.Button(
            self.mainframe,
            text = "Cello",
            command = self.start_command('cello'))
        
        self.btn_dict['xylo'] = ttk.Button(
            self.mainframe,
            text = "Xylo",
            command = self.start_command('xylo'))

        sound_paths = load_sounds.misc()
        commands = [lambda i=i: Thread(target=self.play_sound,
                                     args=(sound_paths[i],)).start() for i in range(6)]

        for e,c in enumerate(commands):
            LOGGER.debug((e,c))
            self.btn_dict['sound'+str(e+1)] = ttk.Button(
                self.mainframe,
                text = os.path.basename(sound_paths[e]).split('.')[0],
                command = c)
    
        LOGGER.debug(self.btn_dict)
        dict_iter = iter(self.btn_dict)
        for j in range(1,4):
            for k in range(1,4):
                btn = self.btn_dict[dict_iter.next()]
                LOGGER.debug(btn['text'])
                btn.grid(column=j, row=k, stick=(W,E))

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
            #while self.wait:
            #    time.sleep(0.1)
            unit = mind.choose_unit()
            unit.play(unit_player)

        self.stop_flag = False
        
    def start_command(self, instr):
        return lambda: Thread(target=self.play, args=(instr,)).start()

    def stop(self, instr):
        self.stop_dict[instr] = True
        self.btn_dict[instr]['command'] = self.start_command(instr)

    def play_sound(self, sound):
        LOGGER.debug(sound)
        playsound(sound, False)
        #self.btn_dict['sound'+str(sound)]['command'] = self.stop
    
if __name__ == "__main__":
    argparser = ArgumentParser()
    max_instr = 5
    argparser.add_argument("instrument", choices=["piano","cello","xylo"], nargs=1)
    args = argparser.parse_args()
    app = App()
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        LOGGER.error("exiting")
        
        


        
