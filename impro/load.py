import csv

mapping = {}
with open('mappings.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ' ')
    
    for row in reader:
        seq = tuple(e for e in row['seq_type_mode'].split(','))
        mapping[seq] = tuple(int(i) for i in row['tones'].split(','))
    

