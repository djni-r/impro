class Note:
    def __init__(self, pitch, octave, duration, volume, touch_type):
        self.pitch = pitch
        self.octave = octave
        self.duration = duration
        self.volume = volume
        self.touch_type = touch_type
        
    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.pitch, 
                                       self.octave, 
                                       self.duration, 
                                       self.volume, 
                                       self.touch_type)


class Pattern:
    def __init__(self, form, pat_type):
        self.form = form
        self.type = type
        
     
class Sequence:
    '''
    Describes sequence of notes or patterns
    seq_type: (scale, triad_arpeggio, sixth_arpeggio, seventh_arpeggio)
    span: 1, 2 bars, 1/2, 2/3 of a bar etc.
    '''        
    def __init__(self, seq_type, span):
        self.type = type
        self.span = span