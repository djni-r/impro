import random
import math
from objects import *
from classes import *

# choose key, rhythm
# rhythm = random.choice(rhythms)
key = random.choice(keys)
mode = random.choice(modes)

# start rhythm
while True:

    # pattern or not
#    is_pattern = random.randint(0, 1)
    
    # in or out of tune
#    in_tune = random.randint(0, 1)
    
    # choose note (pitch, octave, value, volume, touch_type)
    note = Note(random.choice(keys),
                math.floor(random.normalvariate(0.35, 0.35) * 10),
                random.choice(durations),
                random.choice(volumes),
                random.choice(articulations))

     # choose sequence
    if (random.random() < 0.2):
        seq = Sequence(random.choice(seq_types),
                       random.choice(seq_span_bars),
                       note)

        
        play(seq)
    else:
        play(note)

    if (random.random() < 0.05):
        break

    

    
def play(entity):
    print(entity)
