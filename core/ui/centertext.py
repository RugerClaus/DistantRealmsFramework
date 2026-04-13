from core.ui.font import FontEngine

class CenterText:
    def __init__(self,system):
        self.system = system
        self.font = FontEngine(40).font

    def _draw_centered_text(self, text):
        lines = text.split("\n")
        surface_height = self.system.window.get_height()
        surface_width = self.system.window.get_width()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 255))
            rect = surf.get_rect(center=(surface_width // 2,
                                         start_y + i * self.font.get_height() * 1.1))
            self.system.window.blit(surf, rect)
