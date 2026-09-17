class ButtonRenderer:

    def __init__(self, system):
        self.system = system

    def draw(self, button, target=None):

        if target is None:
            target = self.system.window

        style = button.styles[button.state.state]

        rect = button.rect

        if style.border:
            self.system.window.draw_rect(
                target,
                style.border,
                rect.inflate(
                    style.border_width * 2,
                    style.border_width * 2
                ),
                border_radius=style.border_radius + style.border_width
            )

        if style.background:
            background_rect = rect.inflate(
                -style.border_width * 2,
                -style.border_width * 2
            )

            self.system.window.draw_rect(
                target,
                style.background,
                background_rect,
                border_radius=style.border_radius
            )

        text_rect = button.text_surface.get_rect(
            center=rect.center
        )

        target.blit(
            button.text_surface,
            text_rect
        )