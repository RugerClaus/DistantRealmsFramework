class ButtonRenderer:

    def __init__(self, system):
        self.system = system


    def draw(self, button):

        style = button.styles[button.state.state]

        button.surface.fill((0,0,0,0))


        if style.background:

            self.system.window.draw_rect(
                button.surface,
                style.background,
                button.surface.get_rect(),
                border_radius=style.border_radius,
                object="Button"
            )


        if style.border:

            self.system.window.draw_rect(
                button.surface,
                style.border,
                button.surface.get_rect(),
                width=style.border_width,
                border_radius=style.border_radius,
                object="Button"
            )


        button.surface.blit(
            button.text_surface,
            button.text_rect
        )

        self.system.window.blit(
            button.surface,
            button.rect
        )