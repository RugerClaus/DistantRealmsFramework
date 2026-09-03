class Font:

    def __init__(self, system, font, size):
        self.system = system
        self.font = system.backend.pygame.font.Font(font,size)

    def render(self, *args, **kwargs):
        surface = self.font.render(*args, **kwargs)
        return self.system.backend.draw.Surface.from_pygame(
            self.system,
            surface
        )

    def get_height(self):
        return self.font.get_height()

    def get_linesize(self):
        return self.font.get_linesize()