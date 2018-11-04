import csv
import os
        
def combine(tone_pos, tones):
    for pos in tone_pos:
        yield tones[pos]
        
mapping = {}
with open(os.path.dirname(__file__)+'/resources/modes.csv') as modes, \
open(os.path.dirname(__file__)+'/resources/sequences.csv') as seqs:
    seqs_reader = csv.DictReader(seqs, delimiter = ' ')
    modes_reader = list(csv.DictReader(modes, delimiter = ' '))
        
    for row in seqs_reader:
        seq_type = row['seq_type']
        tone_pos = tuple(int(i) - 1 for i in row['tone_pos'].split(','))
        
        for row in iter(modes_reader):
            tones = tuple(int(i) for i in row['tones'].split(','))
            mapping[(seq_type, row['mode'])] = tuple(
                i for i in combine(tone_pos, tones))



