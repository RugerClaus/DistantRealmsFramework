from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine

class Label(UIElement):
    def __init__(self, system, id, text, position):
        super().__init__(position=position)
        self.system = system
        self.id = id
        self.font = FontEngine(30).font
        self.text = text
        self.type = WIDGET.LABEL
        self.scale()

    def scale(self):
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
            (255,255,255)
        )

        rect = surf.get_rect(center=self.rect.center)

        self.system.window.blit(surf, rect)