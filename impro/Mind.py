import random
import math
import copy
import itertools
from collections import deque
from threading import Thread

import numpy as np
from numpy import random as nprand

from impro.ProbCalc import ProbCalc
from impro.Listener import Listener
from impro.Rhythm import Rhythm
from impro.Sequence import Sequence
from impro.probs import *
from impro.objects import *
from impro.unit import *
from impro.load_mapping import mapping


class Mind(object):
    def __init__(self, instrument = "piano", key = None, mode = None,
                 beat = (4,4), bpm = 60, max_mem = None,
                 max_octave = 5, max_tone = 12, min_octave = 1, min_tone = 1):
        self.instrument = instrument
        self.key = key if key else random.choice(keys)
        self.mode = mode if mode else random.choice(modes)
        self.rhythm = Rhythm(beat, bpm)
                             
        self.units_mem = deque(maxlen = max_mem) 
        self.max_octave = max_octave
        self.max_tone = max_tone
        self.min_octave = min_octave
        self.min_tone = min_tone
        
        self.cur_seq = None
        self.outer_unit = None

        self.listener = Listener()
        self.listener.setDaemon(True)
        self.listener.start()
        self.prob_calc = ProbCalc(self.listener, self.instrument)
        

        
    ''' chooses a unit, being a note or a pattern to be played'''
    def choose_unit(self):
        if random.random() < self.prob_calc.repeat_prob() \
        and len(self.units_mem) > 0:
            notes_count = self.prob_calc.repeat_count(len(self.units_mem))
            pat = Pattern([self.units_mem[i] for i in range(-1*notes_count, 0)])
            return pat
        elif self.cur_seq != None and not self.cur_seq.finished:
            unit = self.__next_in_seq()
            #self.cur_seq.cur_unit = unit
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
            duration = self.prob_calc.durs_probs("pause")
            return Pause(duration)
        
        # choose random note (key, octave, value, volume, touch_type)
        octave = self.prob_calc.oct_probs(self.min_octave, self.max_octave)
        key = nprand.choice(keys, p=self.prob_calc.keys_probs())
        duration = self.prob_calc.durs_probs()
        volume = nprand.choice(volumes, p=vols_probs)
        articul = nprand.choice(articulations, p=arts_probs)

        # inefficient bug correction
        if (octave == self.max_octave and keys_to_nums[key] > self.max_tone):
            key = keys[self.max_tone-1]
        elif (octave == self.min_octave and keys_to_nums[key] < self.min_tone):
            key = keys[self.min_tone-1]
            

        unit = Note(key, octave, duration, volume, articul)

        if random.random() < self.prob_calc.pattern_prob():
            unit.duration = self.prob_calc.durs_probs("pattern")
            pat_form = nprand.choice(pattern_forms,
                                     p=self.prob_calc.pat_form_probs())
            pat_mode = nprand.choice(pattern_modes,
                                     p=self.prob_calc.pat_mode_probs())

            pat_units = self.__prepare_pattern_units(pat_form, pat_mode, unit)
            unit = Pattern(pat_units, pat_form, pat_mode)     

        return unit

    
    def __choose_seq(self, first_unit):
        # choose sequence
        _type = nprand.choice(seq_types, p=seq_types_probs)
        span = nprand.choice(seq_span, p=seq_span_probs)
        key = nprand.choice(keys, p=seq_keys_probs)
        mode = nprand.choice(modes, p=seq_modes_probs)
        direction = nprand.choice(directions, p=seq_dir_probs)
        # choose duration of the first unit, i.e. dur for all units in seq
        first_unit.duration = self.prob_calc.durs_probs("sequence")

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

        rel_octave = int(self.cur_seq.cur_pos / len(tones))
        abs_octave = cur_unit.octave + self.cur_seq.direction * rel_octave

        # xxx_i stands for 'index of xxx' 
        first_key_i = keys.index(self.cur_seq.first_unit.key)        
        # quick fix for not having first tone among the tones
        first_tone_i = tones.index(first_key_i + 1) if first_key_i + 1 in tones \
                       else tones[0]
        
        cur_tone_i = first_tone_i + self.cur_seq.cur_pos
        abs_octave += cur_tone_i/len(tones) * self.cur_seq.direction # 1 or -1
        cur_tone_i %= len(tones)
        cur_tone = tones[cur_tone_i]
        
        if (12*(abs_octave-1) + cur_tone > 12*(self.max_octave-1) + self.max_tone) \
        or (12*(abs_octave-1) + cur_tone < 12*(self.min_octave-1) + self.min_tone):
            # self.cur_seq.direction *= -1
            self.cur_seq.finished = True
            cur_unit = self.choose_unit() # recursion here!
        else:
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
