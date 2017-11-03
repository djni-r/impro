import random
import math
import numpy as np
from collections import deque
from threading import Thread


from Rhythm import Rhythm
from Sequence import Sequence
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
        self.cur_seq = None
        self.max_octave = max_octave
        self.min_octave = min_octave


    ''' chooses a unit, being a note or a pattern '''
    def choose_unit(self):

        if self.cur_seq != None and not self.cur_seq.finished:
            unit = self._next_in_seq()
            self.cur_seq.incr_cur_pos()
        else:
            unit = self._choose_rand_unit()
            self.cur_seq = self._choose_seq(unit)
            
        self.units_mem.append(unit)

        return unit

    
    def _next_in_seq(self):
        map_key = (self.cur_seq.type, self.cur_seq.mode)
        tones = mapping[map_key] # e.g. (1,3,5,8) out of 12     

        if (self.cur_seq.direction == -1):
            tones = tones[::-1]
            
        rel_octave = int(self.cur_seq.cur_pos / len(tones))
        abs_octave = self.cur_seq.first_unit.octave + rel_octave

        cur_tone = tones[self.cur_seq.cur_pos % len(tones)]
        # if sequence span is over one octave e.g. 1 3 5 8 1 3 5 8 1 3 5 8
        # first 1 3 5 8 is tone_octave 0, second 1 3 5 8 is tone_octave 1 etc.
        first_pitch_i = keys.index(self.cur_seq.first_unit.pitch)
        # from ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
        # if first pitch is G, then first_pitch_i = 10
        # if cur_tone is for ex. 5 (G,G#,A,A#,B) -> B (2 in the map 'keys')
        # (10 + 5 - 1) % 12 = 2
        pitch_i = first_pitch_i + cur_tone - 1

        if pitch_i > len(keys):
            abs_octave += 1

        if abs_octave > self.max_octave:
            # self.cur_seq.direction *= -1
            self.cur_seq.finished = True
            unit = self._choose_rand_unit()
        else:
            pitch_i %= len(keys)
            pitch = keys[pitch_i]
                
            duration = self.cur_seq.first_unit.duration
            volume = self.cur_seq.first_unit.volume
            articulation = self.cur_seq.first_unit.articulation
                
            unit = Note(pitch, abs_octave, duration, volume, articulation)

        return unit

    
    def _choose_rand_unit(self):
        # choose random note (pitch, octave, value, volume, touch_type)
        octave = np.random.choice(np.arange(self.min_octave, self.max_octave+1),
                                  p=octave_probs[self.min_octave-1:self.max_octave])
        unit = Note(random.choice(keys),
                    octave,
                    random.choice(durations),
                    random.choice(volumes),
                    random.choice(articulations))

        return unit
        
    def _choose_seq(self, first_note):
        # choose sequence
        if (random.random() < 0.2):
            seq = Sequence(random.choice(seq_types),
                           random.choice(seq_span),
                           random.choice(keys),
                           random.choice(modes),
                           random.choice(directions),
                           first_note)

            seq.incr_cur_pos()
            return seq

    def start_beat(self):
        self.rhythm.setDaemon(True)
        self.rhythm.start()

    
    def stop_beat(self):
        self.rhythm.running = False
