import sys
from Player import Player

if len(sys.argv) > 1 and sys.argv[1] == "cello":
    Player().play_cello()
else:
    Player().play_piano()
