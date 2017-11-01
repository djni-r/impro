class Sequence:
    '''
    Describes sequence of units (notes or patterns)
    seq_type: (scale, triad_arpeggio, sixth_arpeggio, seventh_arpeggio)
    span: measured in number of units
    key: the key of the sequence
    mode: e.g. major, minor, whole-tone etc.
    direction: 1 or -1 (ascending or descending)
    first_unit: first unit (note, pattern) in the sequence
    '''        
    def __init__(self, type, span, key, mode, direction, first_unit):
        self.type = type
        self.span = span
        self.key = key
        self.mode = mode
        self.direction = direction 
        self.first_unit = first_unit
        self.cur_pos = 0
        self._finished = False

    '''current position of the unit in the sequence'''


    @property
    def finished(self):
        return self._finished

    def incr_cur_pos(self):
        self.cur_pos += 1
        if self.cur_pos > self.span:
            self._finished = True

