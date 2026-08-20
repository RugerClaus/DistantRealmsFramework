class ButtonRenderer:

    def __init__(self, system):
        self.system = system

    def draw(self, button, target=None):

        if target is None:
            target = self.system.window

        style = button.styles[button.state.state]

        button.surface.fill((0, 0, 0, 0))

        rect = button.surface.get_rect()

        if style.border:
            self.system.window.draw_rect(button.surface,style.border,rect,border_radius=style.border_radius + style.border_width)

        if style.background:
            background_rect = rect.inflate(-style.border_width * 2, -style.border_width * 2)

            self.system.window.draw_rect(button.surface,style.background,background_rect,border_radius=style.border_radius)

        button.surface.blit(button.text_surface,button.text_rect)

        target.blit(button.surface,button.rect)