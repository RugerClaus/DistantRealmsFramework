from core.util.colors import white, black
from core.ui.element import UIElement


class Tooltip(UIElement):

    def __init__(
        self,
        system,
        text="",
        topright=(0, 0),
        font_size=20,
        padding=8,
        background_color=white,
        text_color=black
    ):

        super().__init__(
            focusable=False,
            position=(0, 0)
        )

        self.system = system
        self.text = str(text)
        self.topright = topright
        self.font_size = int(font_size)
        self.padding = int(padding)
        self.background_color = background_color
        self.text_color = text_color

        self.font = None
        self.surface = None
        self.rect = None

        self.visible = False

        self.scale()

    def set_text(self, text):

        self.text = str(text)
        self.scale()

    def set_topright(self, topright):

        self.topright = topright
        self.scale()

    def show(self):

        self.visible = True
        self.scale()

    def hide(self):

        self.visible = False

    def scale(self):

        self.font = self.system.font.get_font(
            self.font_size
        )

        text_surface = self.font.render(
            self.text,
            False,
            self.text_color
        )

        width = (
            text_surface.get_width()
            + self.padding * 2
        )

        height = (
            text_surface.get_height()
            + self.padding * 2
        )

        self.surface = self.system.window.make_surface(
            width,
            height
        )

        self.rect = self.surface.get_rect(
            topright=self.topright
        )

        self.surface.fill(self.background_color)

        self.system.window.draw_rect(
            self.surface,
            black,
            self.surface.get_rect(),
            1
        )

        text_rect = text_surface.get_rect(
            center=self.surface.get_rect().center
        )

        self.surface.blit(
            text_surface,
            text_rect
        )

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):

        if not self.visible:
            return

        if self.surface is None:
            return

        self.system.window.blit(
            self.surface,
            self.rect
        )