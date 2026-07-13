from core.ui.font import FontEngine

class Label:
    def __init__(self, system, text, x_ratio, y_ratio):
        self.system = system
        self.font = FontEngine(30).font
        self.text = text
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.type = "label"
        self.scale()

    def scale(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        x = int(ww * self.x_ratio)
        y = int(wh * self.y_ratio)

        self.rect = self.font.render(
            self.text,
            False,
            (255,255,255)
        ).get_rect(center=(x, y))

    def draw(self):
        surf = self.font.render(
            self.text,
            False,
            (255,255,255)
        )

        rect = surf.get_rect(center=self.rect.center)

        self.system.window.blit(surf, rect)