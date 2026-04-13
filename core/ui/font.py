import pygame
from helper import asset

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

    def __init__(self, type="default"):
        if isinstance(type, int):
            pygame.font.init()
            size = type
            self.font = pygame.font.Font(asset('default_font'), size)
        else:
            size = self.PRESETS.get(type, self.PRESETS["default"])
            self.font = pygame.font.Font(asset("default_font"), size)
