from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import white
class Query(UIElement):
    def __init__(self, system, id, text, font_size=40, position=(0.5, 0.2)):
        super().__init__(position=position)
        self.system = system
        self.id = id
        self.type = WIDGET.QUERY
        self.text = text
        self.font = FontEngine(font_size).font
        self.x_ratio, self.y_ratio = position
        self.default_color = white
        self.color = self.default_color
        self.scale()

    def set_text(self, text,color = None):
        self.text = text
        self.color = color if color else self.default_color
        self.scale()

    def scale(self):
        x,y = self.get_screen_position()
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self):
        if self.text is None:
            return
        self.system.window.blit(self.surf, self.rect)