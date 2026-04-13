from enum import Enum,auto

class PLAYER_MOVE_STATE(Enum):
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    IDLE = auto()