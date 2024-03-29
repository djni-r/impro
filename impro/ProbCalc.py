import time
import math
from numpy import random as nprand

from impro.objects import keys, durations, durs_range_map

class ProbCalc:
    MAX_SEC_INTERVAL = 10
    KEY_WEIGHT_INCR = 10
    MAX_REPEAT_COUNT = 5
    
    def __init__(self, listener, instrument):
        self.listener = listener
        self.instrument = instrument
        
        
    ''' 
    weights is a sequence of weights not summed to 1
    returns seq summed to 1
    '''
    def calc_prob_from_weights(self, weights):
        denom = sum(weights)/len(weights)
        probs = map(lambda x: x/denom/len(weights), weights)

        return probs


    def durs_probs(self, unit_type = "note"):
        unit_types = durs_range_map[self.instrument]
        probs = durations[durations.index(unit_types[unit_type][0]):\
                          durations.index(unit_types[unit_type][1])]
        return nprand.choice(probs)         


    def keys_probs(self):
        keys_weights = {"C":1, "Db":1, "D":1, "Eb":1,
                        "E":1, "F":1, "Gb":1, "G":1,
                        "Ab":1, "A":1, "Bb":1, "B":1}

        now = time.time()
        
        if len(self.listener.pitches) > 0 \
        and self.listener.pitches[-1].time - now > ProbCalc.MAX_SEC_INTERVAL:        
            key_i = self.listener.pitches[-1].pitch % 12
            key = keys[key_i]
            
            keys_weights[key] += ProbCalc.KEY_WEIGHT_INCR
            return calc_probs_from_weights(keys_weights.values())


    def oct_probs(self, min_oct, max_oct):
        count = max_oct - min_oct + 1
        mu = min_oct + count/2.0
        sig = count/(3*2.0)
        octave = int(round(nprand.normal(mu, sig)))
        if octave < min_oct:
            octave = min_oct
        elif octave > max_oct:
            octave = max_oct

        return octave
        
        
    def pat_form_probs(self):
        return None


    def pat_mode_probs(self):
        return None

    
    def pattern_prob(self):
        return 0.2

    
    def pause_prob(self):
        return 0.1


    def pause_dur_probs(self):
        return None
        

    def repeat_prob(self):
        return 0.1


    def repeat_count(self, mem_len):
        r = range(1, ProbCalc.MAX_REPEAT_COUNT + 1 \
              if ProbCalc.MAX_REPEAT_COUNT < mem_len \
                  else mem_len + 1)
        return nprand.choice(r)


    def seq_durs_probs(self):
        if self.instrument == "cello":
            return self.durs_probs()
        
    def seq_prob(self):
        return 0.2

            
            
        
