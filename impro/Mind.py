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


class Mind(object):
    def __init__(self, key = None, mode = None,
                 beat = (4,4), bpm = 60, max_mem = None,
                 max_octave = 5, min_octave = 1):

        self.key = key if key else random.choice(keys)
        self.mode = mode if mode else random.choice(modes)
        self.rhythm = Rhythm(beat, bpm)
                             
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
            if not isinstance(unit, Pause) and \
            random.random() < self.prob_calc.seq_prob():
                self.cur_seq = self.__choose_seq(unit)

        self.units_mem.append(unit)

        return unit


    def start_beat(self):
        self.rhythm.setDaemon(True)
        self.rhythm.start()

    
    def stop_beat(self):
        self.rhythm.running = False

        
    ''' private functions '''

    # not used
    def __consider_outer(self):
        return False
        

    def __choose_rand_unit(self, considering_outer = False):
        if considering_outer:
            pass

        if random.random() < self.prob_calc.pause_prob():
            duration = nprand.choice(durations, p=self.prob_calc.pause_dur_probs())
            return Pause(duration)
        
        # choose random note (key, octave, value, volume, touch_type)
        octaves = np.arange(self.min_octave, self.max_octave+1)
        _octave_probs = octave_probs[self.min_octave-1:self.max_octave]
        octave = nprand.choice(octaves, p=_octave_probs)
        key = nprand.choice(keys, p=self.prob_calc.keys_probs())
        duration = nprand.choice(durations, p=durs_probs)
        volume = nprand.choice(volumes, p=vols_probs)
        articul = nprand.choice(articulations, p=arts_probs)

        unit = Note(key, octave, duration, volume, articul)

        if random.random() < self.prob_calc.pattern_prob():
            unit.duration = nprand.choice(durations_in_pat)
            pat_form = nprand.choice(pattern_forms,
                                     p=self.prob_calc.pat_form_probs())
            pat_mode = nprand.choice(pattern_modes,
                                     p=self.prob_calc.pat_mode_probs())

            pat_units = self.__prepare_pattern_units(pat_form, pat_mode, unit)
            unit = Pattern(pat_form, pat_mode, pat_units)     

        return unit

    
    def __choose_seq(self, first_unit):
        # choose sequence
        _type = nprand.choice(seq_types, p=seq_types_probs)
        span = nprand.choice(seq_span, p=seq_span_probs)
        key = nprand.choice(keys, p=seq_keys_probs)
        mode = nprand.choice(modes, p=seq_modes_probs)
        direction = nprand.choice(directions, p=seq_dir_probs)
        # choose duration of the first unit, i.e. dur for all units in seq
        first_unit.duration = nprand.choice(durations_in_seq)

        seq = Sequence(_type, span, key, mode, direction, first_unit)
        seq.incr_cur_pos()

        print(seq)
        return seq

    
    def __next_in_seq(self):
        map_key = (self.cur_seq._type, self.cur_seq.mode)
        tones = mapping[map_key] # e.g. (1,3,5,8) out of 12     
        cur_unit = copy.copy(self.cur_seq.cur_unit)
        
        if (self.cur_seq.direction == -1):
            tones = tones[::-1]

        # if sequence span is over more than one octave e.g. 1 3 5 8 1 3 5 8 1 3 5 8
        # first 1 3 5 8 is rel_octave 0, second 1 3 5 8 is rel_octave 1 etc.
        rel_octave = int(self.cur_seq.cur_pos / len(tones))
        abs_octave = cur_unit.octave + self.cur_seq.direction * rel_octave

        # xxx_i stands for 'index of xxx' 
        # from ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
        # if first key is G, then first_key_i = 10
        # if cur_tone is for ex. 5 from (G,G#,A,A#,B) -> B (2 in the map 'keys')
        # (10 + 5 - 1) % 12 = 2
        first_key_i = keys.index(self.cur_seq.first_unit.key)        
        # quick fix for not having first tone among the tones
        first_tone_i = tones.index(first_key_i + 1) if first_key_i + 1 in tones \
                       else tones[0]
        
        cur_tone_i = first_tone_i + self.cur_seq.cur_pos
        abs_octave += cur_tone_i/len(tones) * self.cur_seq.direction # 1 or -1
        cur_tone_i %= len(tones)
            
        if abs_octave > self.max_octave:
            # self.cur_seq.direction *= -1
            self.cur_seq.finished = True
            cur_unit = self.choose_unit() # recursion here!
        else:
            cur_tone = tones[cur_tone_i]
            key = keys[cur_tone - 1]
                                
            cur_unit.key = key
            cur_unit.octave = abs_octave

        if isinstance(cur_unit, Pattern):
            pat_units = self.__prepare_pattern_units(cur_unit.form,
                                         cur_unit.mode,
                                         cur_unit.units[0])
            #for i in range(len(pat_units)):
            cur_unit.units = pat_units

        return cur_unit

    
    def __prepare_pattern_units(self, form, mode, base_unit):
        tones = patterns_to_tones[(form,mode)]
        key_i = keys.index(base_unit.key)
        pat_units = [base_unit]
        for tone in tones[1:]:
            unit = copy.copy(base_unit)
            new_key_i = key_i + tone - 1
            unit.octave += new_key_i/12
            if unit.octave > self.max_octave:
                break
            
            unit.key = keys[new_key_i%12]
            pat_units.append(unit)

        return pat_units
