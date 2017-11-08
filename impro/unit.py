class Note:
    def __init__(self, pitch, octave, duration, volume, articulation):
        self.pitch = pitch
        self.octave = octave
        self.duration = duration
        self.volume = volume
        self.articulation = articulation
        
    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.pitch, 
                                       self.octave, 
                                       self.duration, 
                                       self.volume, 
                                       self.articulation)


class Pattern:
    def __init__(self, form, mode, first_note):
        self.form = form
        self.mode = mode
        self.first_note

    def __str__(self):
        return "{} {} {}".format(self.mode, self.form, self.first_note)
