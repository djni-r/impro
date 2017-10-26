import random
import math

from Mind import Mind

mind = Mind()
unit = None
while True:
    unit = mind.choose_unit()
    print(unit)

    if (random.random() < 0.03):
        break

    
def play(unit):
     print(unit)
