from fractions import Fraction
# haven't decided whether these should be enums or just tuples

beats = [(2,4), (3,4), (4,4)]
keys = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
keys_to_nums = {"C":1, "Db":2, "D":3, "Eb":4,
                "E":5, "F":6, "Gb":7, "G":8,
                "Ab":9, "A":10, "Bb":11, "B":12}

modes = ["major", "minor", "mixolydian"]

# perhaps should divide pattern_forms into interval and form later
pattern_forms = ["terza", "quarta", "quinta", "triad", "sept-chord"]
pattern_modes = ["major", "minor", "in-key"]

seq_types = ["scale", "triad", "sixth", "seventh", "ninth"]
seq_span = list(range(10))
directions = [1, -1] # ascending, descending

durations = ["1/1", "1/2", "1/3", "1/4", "1/6", "1/8", "1/12", "1/16"]

durations_in_seq = ["1/6", "1/8", "1/12", "1/16"]
volumes = range(8)
articulations = ["staccato", "sforzato", "legato"]
