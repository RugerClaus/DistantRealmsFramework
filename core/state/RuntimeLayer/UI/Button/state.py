from enum import Enum, auto

class BUTTON_STATE(Enum):
    IDLE = auto()
    HOVER = auto()
    PRESS = auto()
    DISABLE = auto()
    FOCUSED = auto()