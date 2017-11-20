from impro.Mind import Mind
from vendor.UnitPlayer import UnitPlayer

def play():
    mind = Mind()
    unit_player = UnitPlayer(mind.rhythm.bpm)
    
    mind.start_beat()
    while True:
        unit = mind.choose_unit()
        unit.play(unit_player)
            
if __name__ == "__main__":
    play()


        
