# haven't decided whether these should be enums or just tuples

rhythms = ((2,4), (3,4), (4,4))
keys = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
modes = ("major", "minor")
# perhaps should divide PatternForm into interval and form later
pattern_forms = ("terza", "quarta", "quinta", "triad", "sept_chord") 
pattern_modes = ("major", "minor", "in_key")

seq_types = ("scale", "triad_arpeggio", "sixth_arpeggio", "seventh_arpeggio")
seq_modes = ("major", "minor", "mixolidian")
seq_span_bars = ((1,4), (1,3), (1,2), (1,1))

durations = ((1,1), (1,2), '''(1,3),''', (1,4), '''(1,6),''', (1,8), '''(1,12),''' (1,16))
volumes = range(8)
articulations = ("staccato", "marcato", "legato")
