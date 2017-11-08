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
    def __init__(self, _type, span, key, mode, direction, first_unit):
        self._type = _type
        self.span = span
        self.key = key
        self.mode = mode
        self.direction = direction 
        self.first_unit = first_unit
        self.cur_unit = first_unit
        '''current position of the unit in the sequence'''
        self.cur_pos = 0
        self.finished = False


    def incr_cur_pos(self):
        self.cur_pos += 1
        if self.cur_pos > self.span:
            self.finished = True


    def next(self):
        pass

