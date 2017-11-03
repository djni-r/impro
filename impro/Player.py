import random
import time
import sounddevice as sd

from Mind import Mind
from objects import keys


class Player:

    def __init__(self):
        self.mind = Mind()

    def play_cello(self):
        from load_cello import data, rate
                
        self.mind.start_beat()

        while True:
            unit = self.mind.choose_unit()
            map_key = unit.pitch + str(unit.octave)
            sound = None
            
            if map_key in data:
                sound = data[map_key][random.choice(list(data[map_key].keys()))]

            if sound is not None:
                sd.play(sound, rate)

            time.sleep(self.mind.rhythm.sec_per_beat *
                       unit.duration[0] / unit.duration[1])
            
            if (random.random() < 0.01):
                self.mind.stop_beat()
                break
        
    def play_piano(self):
        from load_sounds import data, rate
        self.mind.start_beat()

        while True:
            unit = self.mind.choose_unit()
            unit_data_i = (12 * (unit.octave - 1) + keys.index(unit.pitch))
            
            print(unit)
            sd.play(data[4 + unit_data_i], rate)
            
            time.sleep(self.mind.rhythm.sec_per_beat *
                       unit.duration[0] / unit.duration[1])
            
#            if (random.random() < 0.01):
#                self.mind.stop_beat()
#                break
            


