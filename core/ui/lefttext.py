from core.ui.font import FontEngine

class LeftAlignedText:
    def __init__(self, system,font_size=None):
        self.system = system
        self.surf = None
        self.rect = None
        self.font_size = font_size if font_size is not None else 30
        if not font_size:
            self.font = FontEngine(self.font_size).font
        else:
            self.font = FontEngine(font_size).font

    def _draw_left_aligned_text(self, text):
        lines = text.split("\n")
        surface_height = self.system.window.get_height()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        margin_left = 50

        for i, line in enumerate(lines):
            self.surf = self.font.render(line, True, (255, 255, 255))
            self.rect = self.surf.get_rect(topleft=(margin_left, start_y + i * self.font.get_height() * 1.1))
            self.system.window.blit(self.surf, self.rect)
