import time
from objects import keys

class ProbCalc:
    def __init__(self, listener):
        self.listener = listener
        
    def seq_prob(self):
        prob = 0.2
        return prob


    def keys_probs(self):
        keys_weights = {"C":1, "Db":1, "D":1, "Eb":1,
                        "E":1, "F":1, "Gb":1, "G":1,
                        "Ab":1, "A":1, "Bb":1, "B":1}

        now = time.time()
        MAX_SEC_INTERVAL = 10
        if len(self.listener.pitches) > 0 \
        and self.listener.pitches[-1].time - now > MAX_SEC_INTERVAL:        
            key_i = self.listener.pitches[-1].pitch % 12
            key = keys[key_i]
            
            keys_weights[key] += 5
            return calc_probs_from_weights(keys_weights.values())


    ''' 
    weights is a sequence of weights not summed to 1
    returns seq summed to 1
    '''
    def calc_prob_from_weights(self, weights):
        denom = sum(weights)/len(weights)
        probs = map(lambda x: x/denom/len(weights), weights)

        return probs
            
            
            
        