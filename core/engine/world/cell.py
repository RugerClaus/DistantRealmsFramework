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

        self.base_color = self.data.get("color", white)
        self.color = self.base_color

        self.properties = self.data.get(
            "properties",
            {}
        )
        self.light_variants = None

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

    def set_lighting_level(self, level):
        if not self.light_variants:
            return

        self.color = self.light_variants[level]

    def create_light_variants(self, levels=16, ambient=0.35):

        if not self.base_color:
            self.light_variants = None
            return

        if levels < 2:
            raise ValueError("Lighting requires at least 2 levels")

        self.light_variants = []

        for index in range(levels):

            brightness = index / (levels - 1)

            light = ambient + (
                (1.0 - ambient) * brightness
            )

            color = tuple(
                int(channel * light)
                for channel in self.base_color
            )

            self.light_variants.append(color)

    def create_light_layers(self):
        if not self.cells:
            return

        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        layer_width = round(ww * self.map_width)
        layer_height = round(wh * self.map_height)

        self.light_layers.clear()

        for level in range(self.lighting_levels):

            surface = self.system.window.make_surface(
                layer_width,
                layer_height,
                True
            )

            surface.fill((0, 0, 0, 0))

            for cell, (column, row) in zip(
                self.cells,
                self.cell_positions
            ):

                if cell.properties.get(
                    "receives_light",
                    False
                ):
                    color = cell.light_variants[level]
                else:
                    color = cell.base_color

                if color:
                    rect = self.get_cell_rect(column, row)

                    surface.fill(
                        color,
                        rect
                    )

            self.light_layers.append(surface)

        self.layer_surface = self.light_layers[
            self.lighting_level
        ]