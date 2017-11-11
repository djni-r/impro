from fractions import Fraction

class Note:
    def __init__(self, pitch, octave, duration, volume = None, articulation = None):
        self.pitch = pitch
        self.octave = octave
        self.duration = Fraction(duration)
        self.volume = volume
        self.articulation = articulation

        
    def __str__(self):
        return "{pitch:2}{octave}-{dur}".format(pitch = self.pitch, 
                                                octave = self.octave, 
                                                dur = self.duration, 
                                                vol = self.volume, 
                                                art = self.articulation)

    
    def __eq__(self, other):      
        if other != None \
        and self.pitch == other.pitch \
        and self.octave == other.octave \
        and self.duration == other.duration \
        and self.volume == other.volume \
        and self.articulation == other.articulation:
            return True
        else:
            return False

        
    def __copy__(self):
        return Note(self.pitch, self.octave, self.duration,
                    self.volume, self.articulation)
        


class Pattern:
    def __init__(self, form, mode, first_note):
        self.form = form
        self.mode = mode
        self.first_note

    def __str__(self):
        return "{} {} {}".format(self.mode, self.form, self.first_note)
