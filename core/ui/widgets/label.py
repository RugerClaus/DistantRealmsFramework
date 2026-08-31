from core.ui.type import WIDGET
from core.ui.element import UIElement

class Label(UIElement):
    def __init__(self, system, id, text, position,font_size=30,color=(255,255,255)):
        super().__init__(position=position)
        self.system = system
        self.id = id
        self.font_size = font_size
        self.text = text
        self.color = color
        self.type = WIDGET.LABEL
        self.scale()

    def scale(self):
        self.font = self.system.font.get_font(self.font_size)
        x,y = self.get_screen_position()

        self.rect = self.font.render(
            self.text,
            False,
            (255,255,255)
        ).get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self):
        surf = self.font.render(
            self.text,
            False,
            (self.color)
        )

        rect = surf.get_rect(center=self.rect.center)

        self.system.window.blit(surf, rect)