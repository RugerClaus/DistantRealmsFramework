from helper import asset
from config import config

class FontEngine:
    PRESETS = {
        "button": 60,
        "UI": 35,
        "debug_state": 20,
        "debug_all_state": 15,
        "game_over": 50,
        "keypress": 50,
        "default": 25
    }

    REFERENCE_WIDTH = 1600
    REFERENCE_HEIGHT = 900

    def __init__(self, system):
        self.system = system
        self.width = 0
        self.height = 0
        self.scale_factor = 1.0
        self.fonts = {}
        self.scale()

    def scale(self, width=None, height=None):
        if width is None:
            width = self.system.window.get_width()

        if height is None:
            height = self.system.window.get_height()

        if width == self.width and height == self.height:
            return

        self.width = width
        self.height = height

        scale_x = width / self.REFERENCE_WIDTH
        scale_y = height / self.REFERENCE_HEIGHT
        self.scale_factor = min(scale_x, scale_y)

        self.fonts.clear()

    def get_font(self, type="default"):
        if isinstance(type, int):
            base_size = type
        else:
            base_size = self.PRESETS.get(type, self.PRESETS["default"])

        if type not in self.fonts:
            size = max(1, round(base_size * self.scale_factor))

            if config["WINDOW_BACKEND"] == "pygame":
                font = self.system.backend.pygame.font.Font(
                    asset("default_font"),
                    size
                )

            elif config["WINDOW_BACKEND"] == "draw":
                font = self.system.backend.draw.Font(
                    self.system,
                    asset("default_font"),
                    size
                )

            self.fonts[type] = font

        return self.fonts[type]