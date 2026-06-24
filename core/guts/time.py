import pygame
class Time:
    def __init__(self):
        self.time = pygame.time #private to keep things clean at least that's what i will intend
        self.clock = pygame.time.Clock()
        self.fps = 60

    def get_fps(self):
        return self.clock.get_fps()

    def get_current_time(self):
        return self.time.get_ticks()
    
    def timer(self):
        return self.clock.tick(self.fps)
    
    def delta_time(self):
        ms = self.timer()
        return ms / 1000.0