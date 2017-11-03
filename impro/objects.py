# haven't decided whether these should be enums or just tuples

beats = ((2,4), (3,4), (4,4))
keys = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
modes = ("major", "minor", "mixolydian")

# perhaps should divide pattern_forms into interval and form later
pattern_forms = ("terza", "quarta", "quinta", "triad", "sept-chord") 
pattern_modes = ("major", "minor", "in-key")

seq_types = ("scale", "triad", "sixth", "seventh", "ninth")
seq_span = range(10)
directions = (1, -1) # ascending, descending

durations = ((1,1), (1,2), (1,3), (1,4), (1,6), (1,8), (1,12), (1,16))
volumes = range(8)
articulations = ("staccato", "sforzato", "legato")

octave_probs = [0.02, 0.03, 0.15, 0.4, 0.4, 0.0, 0.0, 0.0]
