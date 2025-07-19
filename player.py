from itertools import cycle
from typing import NamedTuple



class Player(NamedTuple):
    label : str
    color : str

class Move(NamedTuple):
    row : int
    col : int
    label : str

BOARD_SIZE=3
DEFAULT_PLAYERS=(Player(label="X", color="red"), Player(label="O", color="blue"))
