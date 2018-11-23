import time
import random

from fractions import Fraction

from vendor.UnitPlayer import UnitPlayer

class GraphicUnitPlayer(UnitPlayer):

    def __init__(self, bpm = 60):
        print("begin init GraphicUnitPlayer")
        self.sec_per_beat = 60.0/bpm
        self.tk = __import__('Tkinter')
        self.master = self.tk.Tk()
        self.cs = self.tk.Canvas(self.master, width = 200, height = 200)
        self.cs.pack()
        print("end GUP init")


    def play_note(self, note):
        self.cs.create_rectangle(random.randrange(200), random.randrange(200), random.randrange(200), random.randrange(200), fill = random.choice(["red","yellow","blue"]))
        print("created")
        self.master.update()
        #time.sleep(float(Fraction(note.duration)))
        print("finished play")
        

    def play_pattern(self):
        return

    def play_pause(self, pause):
        time.sleep(self.sec_per_beat * float(Fraction(pause.duration)))
