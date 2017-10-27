import random
import time

from Mind import Mind


class Player:
    
    def play(self):
        mind = Mind()
        mind.start_beat()

        while True:
            unit = mind.choose_unit()
            print(unit)
            
            time.sleep(mind.rhythm.sec_per_beat *
                       unit.duration[0] / unit.duration[1])
            
            if (random.random() < 0.01):
                mind.stop_beat()
                break
            


