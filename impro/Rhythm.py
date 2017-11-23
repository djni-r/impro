import time
from threading import Thread

class Rhythm(Thread):
    def __init__(self, beat, bpm):
        Thread.__init__(self)
        self.beat = beat
        self.bpm = bpm 
        self.sec_per_beat = 60.0/self.bpm
        self.beat_count = 1
        self.bar_count = 0
        self.running = False

    def run(self):
        self.running = True
        start_time = time.time()

        while self.running:
            if self.beat_count == 1:
                #print("_"+str(self.bar_count))
                self.bar_count += 1
                
            #print(self.beat_count)
            
            time.sleep(self.sec_per_beat)
            self.beat_count += 1
            if self.beat_count == self.beat[1] + 1:
                self.beat_count = 1
