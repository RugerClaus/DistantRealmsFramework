from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import red, white, black


class Select(UIElement):
    def __init__(self, system, id, position, options, is_active=False):
        super().__init__(focusable=True, position=position)

        self.system = system
        self.id = id
        self.font = FontEngine(30).font

        self.background_color = white
        self.options = options or []
        self.selected_option = self.options[0] if self.options else None

        self.is_active = is_active
        self.is_open = False

        self.type = WIDGET.SELECT
        self.loaded = False

        self.width = 250
        self.height = 50
        self.option_height = 50
        self.padding = 10
        self.max_visible_options = 3
        self.scroll_offset = 0

        self.surface = None
        self.rect = None
        self.select_rect = None
        self.option_rects = []

        self.scale()

    def contains_point(self, position):
        if self.rect is None:
            return False

        local_pos = (
            position[0] - self.rect.x,
            position[1] - self.rect.y
        )

        return self.select_rect.collidepoint(local_pos)

    def error_back(self):
        self.background_color = red

    def clear_error(self):
        self.background_color = white

    def set_active(self, state):
        self.is_active = state

        if not state:
            self.is_open = False

        self.scale()

    def scale(self):
        x, y = self.get_screen_position()

        dropdown_height = self.height

        if self.is_open:
            dropdown_height += self.max_visible_options * self.option_height

        self.surface = self.system.window.make_surface(
            self.width,
            dropdown_height
        )

        self.rect = self.surface.get_rect(
            midtop=(x, y - self.height // 2)
        )

        self.select_rect = self.surface.get_rect()
        self.select_rect.height = self.height

        self.option_rects = []

        for index in range(self.max_visible_options):
            rect = self.surface.get_rect(
                x=0,
                y=self.height + index * self.option_height,
                width=self.width,
                height=self.option_height
            )

            self.option_rects.append(rect)

    def handle_event(self, event):
        if event.type == self.system.input.mouse_scroll_event():
            self.scroll_offset -= event.y
            self.scroll_offset = max(
                0,
                min(
                    self.scroll_offset,
                    len(self.options) - self.max_visible_options
                )
            )
        if event.type == self.system.input.video_resize_event():
            self.scale()
            return

        if not self.is_active:
            return

        if event.type != self.system.input.mouse_button_down():
            return

        if event.button != 1:
            return

        if self.rect is None:
            return

        mouse_pos = self.system.input.get_mouse_pos()

        local_pos = (
            mouse_pos[0] - self.rect.x,
            mouse_pos[1] - self.rect.y
        )

        if self.select_rect.collidepoint(local_pos):
            self.is_open = not self.is_open
            self.scale()
            return

        if self.is_open:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(local_pos):
                    self.selected_option = self.options[self.scroll_offset + index]
                    self.is_open = False
                    self.scale()
                    return

            self.is_open = False
            self.scale()

    def get_return_string(self):
        return str(self.selected_option) if self.selected_option is not None else ""

    def get_selected(self):
        return self.selected_option

    def set_selected(self, option):
        if option in self.options:
            self.selected_option = option

    def update(self):
        pass

    def draw(self):
        if self.surface is None or self.rect is None:
            return

        self.surface.fill(self.background_color)

        # Main select control
        self.system.window.draw_rect(
            self.surface,
            black,
            self.select_rect,
            2
        )

        if self.selected_option is not None:
            surf = self.font.render(
                str(self.selected_option),
                False,
                black
            )

            text_rect = surf.get_rect(
                midleft=(
                    self.padding,
                    self.select_rect.centery
                )
            )

            self.surface.blit(surf, text_rect)

        # Dropdown arrow
        arrow_x = self.select_rect.right - 20
        arrow_y = self.select_rect.centery

        self.system.window.draw_polygon(
            self.surface,
            black,
            [
                (arrow_x - 7, arrow_y - 3),
                (arrow_x + 7, arrow_y - 3),
                (arrow_x, arrow_y + 5)
            ]
        )

        # Dropdown options
        if self.is_open:
            visible_options = self.options[
                self.scroll_offset:
                self.scroll_offset + self.max_visible_options
            ]

            for index, option in enumerate(visible_options):
                rect = self.option_rects[index]

                self.surface.fill(
                    white,
                    rect
                )

                surf = self.font.render(
                    str(option),
                    False,
                    black
                )

                text_rect = surf.get_rect(
                    midleft=(
                        self.padding,
                        rect.centery
                    )
                )

                self.surface.blit(surf, text_rect)

                self.system.window.draw_rect(
                    self.surface,
                    black,
                    rect,
                    1
                )

        self.system.window.blit(
            self.surface,
            self.rect
        )