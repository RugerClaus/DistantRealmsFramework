from enum import Enum, auto

class FETCH_STATE(Enum):
    IDLE = auto()
    FETCHING = auto()
    ERROR = auto()
    SUCCESS = auto()
    TIMEOUT = auto()
    CANCELLED = auto()