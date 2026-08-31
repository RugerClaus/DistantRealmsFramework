from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.util.colors import white
class Header(UIElement):
    def __init__(self, system, id, text, font_size=60, position=(0.5, 0.1),color=white):
        super().__init__(position=position)
        self.system = system
        self.id = id
        self.type = WIDGET.HEADER
        self.text = text
        self.font_size = font_size
        self.x_ratio, self.y_ratio = position
        self.color = color
        self.scale()

    def set_text(self, text,color = None):
        self.text = text
        self.color = color if color else self.default_color

    def scale(self):
        self.font = self.system.font.get_font(self.font_size)
        x,y = self.get_screen_position()
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self):
        if self.text is None:
            return
        self.system.window.blit(self.surf, self.rect)