######
# This class is for managing backends. This is mostly for visual purposes as DRAW, the Distant Realms Ascended Window is a custom wrapper for OpenGL
# and it basically mimics pygame's API. Or at least it's being designed to do so
# This is to keep the framework contract strict while taking advantage of hardware acceleration
######

import pygame
import core.draw as draw
from OpenGL import GL, GLU
class Backend:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.pygame.font.init()
        self.opengl = GL
        self.openglu = GLU
        self.draw = draw
        self.draw.init()