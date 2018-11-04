import time
import random
from fractions import Fraction

import load_sounds


class UnitPlayer(object):
    keys = { "C":0, "Db":1, "D":2, "Eb":3,
             "E":4, "F":5, "Gb":6, "G":7,
             "Ab":8, "A":9, "Bb":10, "B":11 }
    
    def __init__(self, bpm, printout = True):
        print("init UnitPlayer")
        self.sd = __import__('sounddevice')
        self.bpm = bpm
        self.sec_per_beat = 60.0/self.bpm
        self.printout = printout
        self.sounds = load_sounds.piano()
        
        
    def play_note(self, note):  
        note_data_i = (12 * (note.octave - 1) + self.keys[note.key])
        self.sd.play(self.sounds.data[3 + note_data_i], self.sounds.rate)
        if self.printout:
            print(str(note) + " Piano")
            
        time.sleep(self.sec_per_beat * float(Fraction(note.duration)))


    def play_pause(self, pause):
        if self.printout:
            print(pause)

        time.sleep(self.sec_per_beat * float(Fraction(pause.duration)))


    def play_pattern(self, pattern):
        if self.printout:
            print(pattern)



class CelloUnitPlayer(UnitPlayer):

    def __init__(self, bpm, printout = True):
        self.sdc = __import__('sounddevice')
        self.bpm = bpm
        self.sec_per_beat = 60.0/self.bpm
        self.printout = printout
        self.sounds = load_sounds.cello()
        
        
    def play_note(self, note):
        map_key = note.key + str(note.octave)
        sound = None
            
        if map_key in self.sounds.data:
            sound = self.sounds.data[map_key][random.choice(\
                list(self.sounds.data[map_key].keys()))]

        if sound is not None:
            self.sdc.play(sound, self.sounds.rate)
            if self.printout:
                print(str(note) + " Cello")
            time.sleep(self.sec_per_beat * 3 * float(Fraction(note.duration)))


class XyloUnitPlayer(UnitPlayer):

    def __init__(self, bpm, printout = True):
        self.sdx = __import__('sounddevice')
        UnitPlayer.__init__(self, bpm)
        self.sounds = load_sounds.xylo()


    def play_note(self, note):
        map_key = note.key + str(note.octave)
        self.sdx.play(self.sounds.data[map_key], self.sounds.rate)
        if self.printout:
            print(str(note) + " Xylo")
        time.sleep(self.sec_per_beat * float(Fraction(note.duration)))

        
        
        
