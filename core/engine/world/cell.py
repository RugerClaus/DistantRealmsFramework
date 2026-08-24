from core.util.colors import *


class Cell:
    def __init__(
        self,
        system,
        size=(0.01, 0.01),
        position=(0, 0),
        data=None
    ):
        self.system = system

        self.x, self.y = position
        self.width, self.height = size

        self.data = data or {}

        self.color = self.data.get("color", white)
        self.properties = self.data.get("properties", {})

    def set_color(self, color):
        self.color = color

    def get_rect(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        pixel_x = round(self.x * ww)
        pixel_y = round(self.y * wh)

        width = round(self.width * ww)
        height = round(self.height * wh)

        return self.system.window.Rect(
            pixel_x - width // 2,
            pixel_y - height // 2,
            width,
            height
        )

    def update(self):
        pass