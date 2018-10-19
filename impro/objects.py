beats = [(2,4), (3,4), (4,4)]
keys = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
keys_to_nums = {
    "C":1, "Db":2, "D":3, "Eb":4,
    "E":5, "F":6, "Gb":7, "G":8,
    "Ab":9, "A":10, "Bb":11, "B":12
}

modes = ["major", "minor", "mixolydian", "lydian", "dorian", "locrian"]

# perhaps should divide pattern_forms into interval and form later
pattern_forms = ["seconda", "terza", "quarta", "quinta", "sexta", "septima",  "triad"]
pattern_modes = ["major", "minor"]
patterns_to_tones = {
    ("seconda", "minor") : [1,2],
    ("seconda", "major") : [1,3],
    ("terza", "minor") : [1,4],
    ("terza", "major") : [1,5],     
    ("quarta", "minor") : [1,6],
    ("quarta", "major") : [1,7],
    ("quinta", "minor") : [1,8],
    ("quinta", "major") : [1,9],
    ("sexta", "minor") : [1,10],
    ("sexta", "major") : [1,11],
    ("septima", "minor") : [1,12],
    ("septima", "major") : [1,13],
    ("triad", "minor") : [1,4,8],
    ("triad", "major") : [1,5,8]
}

seq_types = ["scale", "triad", "sixth", "seventh", "ninth"]
seq_span = list(range(10))
directions = [1, -1] # ascending, descending

durations = [ "2/1", "1/1", "1/2", "1/3", "1/4", "1/6",
              "1/8", "1/12", "1/16", "1/24",  "1/32" ]

durs_range_map = { "cello" : ("2/1", "1/8"),
                   "note" : ("2/1", "1/32"),
                   "pause" : ("2/1", "1/32"),
                   "pattern" : ("1/12", "1/32"),
                   "sequence" : ("1/12", "1/32") }

volumes = range(8)
articulations = ["staccato", "sforzato", "legato"]
