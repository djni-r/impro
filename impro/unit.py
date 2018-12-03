import copy
from fractions import Fraction


class Note(object):
    def __init__(self, key, octave, duration, volume = None, articulation = None):
        self.key = key
        self.octave = octave
        self.duration = Fraction(duration)
        self.volume = volume
        self.articulation = articulation
        self._units = None

    @property
    def units(self):
        self._units = [self]
        return self._units

    @units.setter
    def units(self, value):
        self._units = value
    
        
    def play(self, vendor):
        vendor.play_note(self)

        
    def __str__(self):
        return "{key:2}{octave}-{dur}".format(key = self.key, 
                                                octave = self.octave, 
                                                dur = self.duration, 
                                                vol = self.volume, 
                                                art = self.articulation)

    
    def __eq__(self, other):      
        if other != None \
        and self.key == other.key \
        and self.octave == other.octave \
        and self.duration == other.duration \
        and self.volume == other.volume \
        and self.articulation == other.articulation:
            return True
        else:
            return False

    
    def __copy__(self):
        return Note(self.key, self.octave, self.duration,
                    self.volume, self.articulation)
        


class Pattern(object):
    
    def __init__(self, units, form = None, mode = None):
        
        self.form = form
        self.mode = mode
        self.units = units
        self._key = units[0].key
        self._octave = units[0].octave
        print("init pattern")
        
    @property
    def key(self):
        return self._key


    @key.setter
    def key(self, value):
        self._key = value

        
    @property
    def octave(self):
        return self._octave


    @octave.setter
    def octave(self, value):
        self._octave = value

    
    def play(self, vendor):
        self.__str__()
        for unit in self.units:
            unit.play(vendor)

        

    def __eq__(self, other):
        if other != None \
        and self.form == other.form \
        and self.mode == other.mode \
        and self.units == other.units:
            return True
        else:
            return False
        

    def __copy__(self):
        units = []
        for unit in self.units:
            units.append(unit.__copy__())

        return Pattern(units, self.form, self.mode)

    
    def __str__(self):
        content = "Pattern {} {} units: ".format(self.mode, self.form)
        for unit in self.units:
            content += str(unit) + " "

        return content + "\n"

    

class Pause(object):
    def __init__(self, duration):
        self.duration = Fraction(duration)
        self._units = None
        self._key = "-"
        self._octave = 0
        


    @property
    def units(self):
        self._units = [self]
        return self._units

    
    @units.setter
    def units(self, value):
        self._units = value


    @property
    def key(self):
        return self._key


    @key.setter
    def key(self, value):
        self.key = "-"


    @property
    def octave(self):
        return self._octave


    @octave.setter
    def octave(self, value):
        sef._octave = 0

        
    def play(self, vendor):
        vendor.play_pause(self)

        
    def __str__(self):
        return "{} pause".format(self.duration)

        
