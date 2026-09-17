from core.ui.type import WIDGET
from core.ui.element import UIElement

class Label(UIElement):
    def __init__(self, system, id, text, position, font_size=30, color=(255,255,255)):
        super().__init__(position=position)
        self.system = system
        self.id = id
        self.font_size = font_size
        self._text = text
        self.color = color
        self.type = WIDGET.LABEL
        self.surface = None
        self.scale()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,value):
        if value == self._text:
            return

        self._text = value

        if hasattr(self,"font"):
            self.render_text()

    def scale(self):
        self.font = self.system.font.get_font(self.font_size)
        self.render_text()

    def render_text(self):
        rendered = self.font.render(
            self.text,
            False,
            self.color
        )

        if self.surface is None or self.surface.get_size() != rendered.get_size():
            self.surface = rendered
        else:
            self.surface.fill((0,0,0,0))
            self.surface.blit(rendered,(0,0))

        x,y = self.get_screen_position()
        self.rect = self.surface.get_rect(center=(x,y))

        self.system.window.mark_surface_dirty(self.surface)

    def update(self):
        pass

    def draw(self):
        self.system.window.blit(self.surface,self.rect)