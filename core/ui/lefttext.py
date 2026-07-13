from core.ui.font import FontEngine


class LeftAlignedText:
    def __init__(self, system, font_size=None):
        self.system = system
        self.surf = None
        self.rect = None

        self.font_size = font_size if font_size is not None else 30
        self.font = FontEngine(self.font_size).font

    def normalized_to_pixel(self, x, y):
        return (
            int(x * self.system.window.get_width()),
            int(y * self.system.window.get_height())
        )

    def _draw_left_aligned_text(self, text):
        lines = text.split("\n")

        screen_height = self.system.window.get_height()

        line_height = self.font.get_height()

        # Normalized layout values
        left_margin = 0.05
        center_y = 0.5
        line_spacing = 0.012

        total_height = (
            len(lines) * line_height +
            (len(lines) - 1) * screen_height * line_spacing
        )

        _, center_pixel_y = self.normalized_to_pixel(
            0,
            center_y
        )

        start_y = int(center_pixel_y - total_height / 2)

        start_x, _ = self.normalized_to_pixel(
            left_margin,
            0
        )

        for i, line in enumerate(lines):

            self.surf = self.font.render(
                line,
                True,
                (255, 255, 255)
            )

            self.rect = self.surf.get_rect(
                topleft=(
                    start_x,
                    start_y + int(
                        i * (
                            line_height +
                            screen_height * line_spacing
                        )
                    )
                )
            )

            self.system.window.blit(
                self.surf,
                self.rect
            )