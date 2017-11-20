import time
import sounddevice as sd
from fractions import Fraction
from load_sounds import data, rate


class UnitPlayer(object):

    def __init__(self, bpm, printout = True):
        self.bpm = bpm
        self.sec_per_beat = 60.0/self.bpm
        self.printout = printout
        self.sounds = []
        self.keys = ["C", "Db", "D", "Eb",
                     "E", "F", "Gb", "G",
                     "Ab", "A", "Bb", "B"]
        
        
    def play_note(self, note):
        
        note_data_i = (12 * (note.octave - 1) + self.keys.index(note.key))
        sd.play(data[4 + note_data_i], rate)
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

        


        
