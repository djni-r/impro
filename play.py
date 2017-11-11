import sys
from impro.Player import Player

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cello":
        Player().play_cello()
    else:
        Player().play_piano()
