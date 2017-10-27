import random
import math
from collections import deque
from threading import Thread

from Rhythm import Rhythm
from Sequence import Sequence
from objects import *
from unit import *
from load import mapping


class Mind:
    def __init__(self, key = None, mode = None,
                 rhythm = None, max_mem = None):

        self.key = key if key else random.choice(keys)
        self.mode = mode if mode else random.choice(modes)
        self.rhythm = rhythm if rhythm else \
                      Rhythm(random.choice(beats),
                             random.randint(60, 240))
                             
        self.units_mem = deque(maxlen = max_mem) 
        self.cur_seq = None
        self.beat = None


    ''' chooses a unit, being a note or a pattern '''
    def choose_unit(self):

        if self.cur_seq != None:
            map_key = tuple([self.cur_seq.type, self.cur_seq.mode])
            tones = mapping[map_key] # e.g. (1,3,5,8) out of 12 tones
            cur_tone = tones[self.cur_seq.cur_pos % len(tones)]
            # if sequence span is over one octave e.g. 1 3 5 8 1 3 5 8 1 3 5 8
            # first 1 3 5 8 is tone_octave 0, second 1 3 5 8 is tone_octave 1 etc.
            first_pitch_i = keys.index(self.cur_seq.first_unit.pitch)
            # from ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
            # if first pitch is G, then first_pitch_i = 10
            # if cur_tone is for ex. 5 (G,G#,A,A#,B) -> B (2 in the map 'keys')
            # (10 + 5 - 1) % 12 = 2
            pitch_i = (first_pitch_i + cur_tone - 1) % len(keys)
            pitch = keys[pitch_i]

            rel_octave = int(self.cur_seq.cur_pos / len(tones))
            abs_octave = self.cur_seq.first_unit.octave + rel_octave

            duration = self.cur_seq.first_unit.duration
            volume = self.cur_seq.first_unit.volume
            articulation = self.cur_seq.first_unit.articulation

            unit = Note(pitch, abs_octave, duration, volume, articulation)
            
            self.cur_seq.incr_cur_pos()
            
            if self.cur_seq.finished:
                self.cur_seq = None
                
        else:
            unit = self.choose_rand_unit()
            self.cur_seq = self.choose_seq(unit)
            
        self.units_mem.append(unit)

        return unit

    def choose_rand_unit(self):
        # choose random note (pitch, octave, value, volume, touch_type)
        rand = random.normalvariate(0.4, 0.15)
        octave = (abs(int(rand * 10)) + 1) % 9
        unit = Note(random.choice(keys),
                    octave,
                    random.choice(durations),
                    random.choice(volumes),
                    random.choice(articulations))

        return unit
        
    def choose_seq(self, first_note):
        # choose sequence
        if (random.random() < 0.2):
            seq = Sequence(random.choice(seq_types),
                           random.choice(seq_span),
                           random.choice(keys),
                           random.choice(modes),
                           random.choice(directions),
                           first_note)

            return seq

    def start_beat(self):
        self.rhythm.start()
        

    def stop_beat(self):
        self.rhythm.running = False
