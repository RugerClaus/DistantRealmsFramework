from core.ui.font import FontEngine


class CenterText:
    def __init__(self, system):
        self.system = system
        self.font = FontEngine(40).font

    def normalized_to_pixel(self, x, y):
        """
        Convert normalized coordinates (0.0 - 1.0)
        into screen pixel coordinates.
        """
        return (
            int(x * self.system.window.get_width()),
            int(y * self.system.window.get_height())
        )

    def _draw_centered_text(self, text):
        lines = text.split("\n")

        surface_height = self.system.window.get_height()

        line_height = self.font.get_height()

        # Normalized layout values
        center_x = 0.5
        center_y = 0.5
        line_spacing = 0.012

        total_height = (
            len(lines) * line_height +
            (len(lines) - 1) * surface_height * line_spacing
        )

        center_pixel_x, center_pixel_y = self.normalized_to_pixel(
            center_x,
            center_y
        )

        start_y = int(
            center_pixel_y - total_height / 2
        )

        for i, line in enumerate(lines):

            surf = self.font.render(
                line,
                True,
                (255, 255, 255)
            )

            rect = surf.get_rect(
                center=(
                    center_pixel_x,
                    start_y + int(
                        i * (
                            line_height +
                            surface_height * line_spacing
                        )
                    )
                )
            )

            self.system.window.blit(
                surf,
                rect
            )