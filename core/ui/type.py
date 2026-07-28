from enum import Enum,auto

class WIDGET(Enum):
    QUERY = auto()
    TEXTBOX = auto()
    LABEL = auto()
    BUTTON = auto()
    FORM = auto()
    IMAGE = auto()
    SCROLLABLETEXT = auto()
    CENTERTEXT = auto()

class COMPOSABLE(Enum):
    FORM = auto()
    MENU = auto()