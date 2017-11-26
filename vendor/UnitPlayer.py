import time
import random
import sounddevice as sd
from fractions import Fraction

import load_sounds


class UnitPlayer(object):
    keys = ["C", "Db", "D", "Eb",
            "E", "F", "Gb", "G",
            "Ab", "A", "Bb", "B"]
    
    def __init__(self, bpm, printout = True):
        self.bpm = bpm
        self.sec_per_beat = 60.0/self.bpm
        self.printout = printout
        self.sounds = load_sounds.piano()
        
        
    def play_note(self, note):  
        note_data_i = (12 * (note.octave - 1) + self.keys.index(note.key))
        sd.play(self.sounds.data[4 + note_data_i], self.sounds.rate)
        if self.printout:
            print(note)
            
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
            sd.play(sound, self.sounds.rate)
            if self.printout:
                print(note)
            time.sleep(self.sec_per_beat * 3 * float(Fraction(note.duration)))
