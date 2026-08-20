######
# THIS CLASS WILL REPLACE ALL PYGAME CALLS IN THE SYSTEM INTERFACE OBJECTS TO MOVE PYGAME BACK A LAYER IN 
# PREPARATION FOR ADDING SUPPORT FOR MULTIPLE BACKENDS
#
# FOR NOW IT WILL SOLEY INITIALIZE PYGAME
######

import pygame
class PGInterface:
    def __init__(self):
        import pygame
        self.pygame = pygame
        pygame.init()

