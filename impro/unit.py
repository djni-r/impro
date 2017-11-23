import copy
from fractions import Fraction


class Note(object):
    def __init__(self, key, octave, duration, volume = None, articulation = None):
        self.key = key
        self.octave = octave
        self.duration = Fraction(duration)
        self.volume = volume
        self.articulation = articulation

        
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
        Pattern.octave = BaseUnitDescr("octave", units[0])
        Pattern.key = BaseUnitDescr("key", units[0])
        
        self.form = form
        self.mode = mode
        self.units = units
        
     
    def play(self, vendor):
        self.__str__()
        for unit in self.units:
            unit.play(vendor)
        #vendor.play_pattern(self)
        

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

        return content

    

class Pause(object):
    def __init__(self, duration):
        self.duration = Fraction(duration)

        
    def play(self, vendor):
        vendor.play_pause(self)

        
    def __str__(self):
        return "{} pause".format(self.duration)



class BaseUnitDescr(object):
    """ 
    DECSRIPTOR FOR PATTERN
    reads and assigns values from/to the base_unit of the Pattern
    """
    def __init__(self, name, base_unit):
        self.name = name
        self.base_unit = base_unit
        

    def __get__(self, obj, objtype):
        return self.base_unit.__getattribute__(self.name)

    
    def __set__(self, obj, val):
        self.base_unit.__setattr__(self.name, val)
        
