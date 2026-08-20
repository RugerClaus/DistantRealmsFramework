
class Time:
    def __init__(self,system):
        self.system = system
        self.backend_time = self.system.backend.pygame.time
        self.backend_clock = self.system.backend.pygame.time.Clock()
        self.fps = 60
        self.dt = 0

    def get_fps(self):
        return self.clock.get_fps()

    def get_current_time(self):
        return self.backend_time.get_ticks()

    def timer(self):
        self.dt = self.backend_clock.tick(self.fps) / 1000.0
        return self.dt

    def delta_time(self):
        return self.dt