from core.ui.type import WIDGET
from core.ui.element import UIElement
from helper import asset

class Image(UIElement):
    def __init__(self, system, id, image, position=(0.5, 0.5), scale=None):
        super().__init__(position=position)

        self.system = system
        self.id = id
        self.type = WIDGET.IMAGE

        self.image = asset(image)

        if self.image is None:
            raise ValueError(f"Unknown image asset: {image}")

        self.x_ratio, self.y_ratio = position
        self.scale_ratio = scale

        self.original_surf = self.system.window.load_image(self.image)
        self.surf = self.original_surf
        self.rect = self.surf.get_rect()

        self.scale()

    def scale(self):
        x, y = self.get_screen_position()

        if self.scale_ratio:
            width = int(self.system.window.get_width() * self.scale_ratio)
            factor = width / self.original_surf.get_width()
            height = int(self.original_surf.get_height() * factor)

            self.surf = self.system.window.transform_scale(
                self.original_surf,
                width,
                height
            )

        else:
            self.surf = self.original_surf

        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self):
        self.system.window.blit(self.surf, self.rect)