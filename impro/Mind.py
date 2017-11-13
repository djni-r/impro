import random
import math
import copy
from collections import deque
from threading import Thread

import numpy as np
from numpy import random as nprand

from ProbCalc import ProbCalc
from Listener import Listener
from Rhythm import Rhythm
from Sequence import Sequence
from probs import *
from objects import *
from unit import *
from load_mapping import mapping


class Mind:
    def __init__(self, key = None, mode = None,
                 beat = (4,4), tempo = 60, max_mem = None,
                 max_octave = 5, min_octave = 1):

        self.key = key if key else random.choice(keys)
        self.mode = mode if mode else random.choice(modes)
        self.rhythm = Rhythm(beat, tempo)
                             
        self.units_mem = deque(maxlen = max_mem) 
        self.max_octave = max_octave
        self.min_octave = min_octave
        
        self.cur_seq = None
        self.outer_unit = None

        self.listener = Listener()
        self.listener.setDaemon(True)
        self.listener.start()
        self.prob_calc = ProbCalc(self.listener)
        

        
    ''' chooses a unit, being a note or a pattern to be played'''
    def choose_unit(self):

        if self.cur_seq != None and not self.cur_seq.finished:
            unit = self.__next_in_seq()
            self.cur_seq.incr_cur_pos()
        else:
            unit = self.__choose_rand_unit(self.__consider_outer())
            if (random.random() < self.prob_calc.seq_prob()):
                self.cur_seq = self.__choose_seq(unit)
            
        self.units_mem.append(unit)

        return unit


    def start_beat(self):
        self.rhythm.setDaemon(True)
        self.rhythm.start()

    
    def stop_beat(self):
        self.rhythm.running = False

        
    ''' private functions '''
    
    def __consider_outer(self):
        return False
        

    def __choose_rand_unit(self, considering_outer = False):
        if considering_outer:
            pass

        # choose random note (pitch, octave, value, volume, touch_type)
        octaves = np.arange(self.min_octave, self.max_octave+1)
        _octave_probs = octave_probs[self.min_octave-1:self.max_octave]
        octave = nprand.choice(octaves, p=_octave_probs)
        key = nprand.choice(keys, p=self.prob_calc.keys_probs())
        duration = nprand.choice(durations, p=durs_probs)
        volume = nprand.choice(volumes, p=vols_probs)
        articul = nprand.choice(articulations, p=arts_probs)

        unit = Note(key, octave, duration, volume, articul)

        return unit

    
    def __choose_seq(self, first_unit):
        # choose sequence
        _type = random.choice(seq_types)
        span = random.choice(seq_span)
        key = random.choice(keys)
        mode = random.choice(modes)
        direction = random.choice(directions)
        # choose duration of the first unit, i.e. dur for all units in seq
        first_unit.duration = random.choice(durations_in_seq)

        seq = Sequence(_type, span, key, mode, direction, first_unit)
        seq.incr_cur_pos()

        print(seq)
        return seq

    
    def __next_in_seq(self):
        map_key = (self.cur_seq._type, self.cur_seq.mode)
        tones = mapping[map_key] # e.g. (1,3,5,8) out of 12     

        if (self.cur_seq.direction == -1):
            tones = tones[::-1]

        # if sequence span is over more than one octave e.g. 1 3 5 8 1 3 5 8 1 3 5 8
        # first 1 3 5 8 is rel_octave 0, second 1 3 5 8 is rel_octave 1 etc.
        rel_octave = int(self.cur_seq.cur_pos / len(tones))
        abs_octave = self.cur_seq.first_unit.octave + \
                     self.cur_seq.direction * rel_octave

        # xxx_i stands for index of xxx 
        # from ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
        # if first pitch is G, then first_pitch_i = 10
        # if cur_tone is for ex. 5 from (G,G#,A,A#,B) -> B (2 in the map 'keys')
        # (10 + 5 - 1) % 12 = 2
        first_pitch_i = keys.index(self.cur_seq.first_unit.pitch)        
        first_tone_i = tones.index(first_pitch_i + 1)
        cur_tone_i = first_tone_i + self.cur_seq.cur_pos
        
        if cur_tone_i >= len(tones):
            abs_octave += self.cur_seq.direction # 1 or -1
            cur_tone_i %= len(tones)
            
        if abs_octave > self.max_octave:
            # self.cur_seq.direction *= -1
            self.cur_seq.finished = True
            unit = self.choose_unit() # recursion here!
        else:
            cur_tone = tones[cur_tone_i]
            pitch = keys[cur_tone - 1]
                                
            unit = copy.copy(self.cur_seq.cur_unit)
            unit.pitch = pitch
            unit.octave = abs_octave

        return unit

    
