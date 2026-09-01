from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.util.colors import red, white, black
import ast


class Select(UIElement):

    def __init__(self, system, id, position, options, selected_option=None, font_size=30, width=0.25, height=0.05, padding=10, max_visible_options=3, is_active=False):
        super().__init__(focusable=True, position=position)
        self.system = system
        self.id = id
        self.font_size = int(font_size)
        self.background_color = white
        self.options = self.normalize_options(options)

        if selected_option in self.options:
            self.selected_option = selected_option
        else:
            self.selected_option = self.options[0] if self.options else None

        self.normalize_boolean_options()
        self.is_active = is_active
        self.is_open = False
        self.type = WIDGET.SELECT
        self.loaded = False
        self.width = float(width)
        self.height = float(height)
        self.padding = int(padding)
        self.max_visible_options = int(max_visible_options)
        self.scroll_offset = 0
        self.surface = None
        self.rect = None
        self.select_rect = None
        self.option_rects = []
        self.scale()

    def normalize_options(self, options):
        if options is None:
            return []

        if isinstance(options, str):
            try:
                parsed = ast.literal_eval(options)

                if isinstance(parsed, (list, tuple)):
                    return list(parsed)

                return [str(parsed)]
            except (ValueError, SyntaxError):
                return [options]

        if isinstance(options, (list, tuple)):
            return list(options)

        return [options]

    def normalize_boolean_options(self):
        if not self.is_boolean_select():
            return

        true_option = None
        false_option = None

        for option in self.options:
            normalized = str(option).strip().lower()

            if normalized == "true":
                true_option = option
            elif normalized == "false":
                false_option = option

        if true_option is None or false_option is None:
            return

        if self.selected_option is True or str(self.selected_option).strip().lower() == "true":
            self.options = [true_option, false_option]
        elif self.selected_option is False or str(self.selected_option).strip().lower() == "false":
            self.options = [false_option, true_option]

    def is_boolean_select(self):
        if len(self.options) != 2:
            return False

        normalized = {str(option).strip().lower() for option in self.options}
        return normalized == {"true", "false"}

    def contains_point(self, position):
        if self.rect is None:
            return False

        if self.select_rect.collidepoint(position):
            return True

        if self.is_open:
            for rect in self.option_rects:
                if rect.collidepoint(position):
                    return True

        return False

    def error_back(self):
        self.background_color = red

    def clear_error(self):
        self.background_color = white

    def set_active(self, state):
        self.is_active = state

        if not state:
            self.is_open = False

        self.scale()

    def set_padding(self, padding):
        self.padding = int(padding)
        self.scale()

    def set_options(self, options):
        old_value = self.selected_option
        self.options = self.normalize_options(options)

        if not self.options:
            self.selected_option = None
        elif old_value in self.options:
            self.selected_option = old_value
        else:
            self.selected_option = self.options[0]

        self.normalize_boolean_options()
        self.scroll_offset = 0
        self.scale()

    def set_selected(self, option):
        if option not in self.options:
            return

        self.selected_option = option
        self.normalize_boolean_options()
        self.scroll_offset = 0
        self.scale()

    def set_value(self, value):
        if value in self.options:
            self.selected_option = value
        elif isinstance(value, bool):
            target = str(value).lower()

            for option in self.options:
                if str(option).strip().lower() == target:
                    self.selected_option = option
                    break
            else:
                return
        else:
            return

        self.normalize_boolean_options()
        self.scroll_offset = 0
        self.scale()

    def set_width(self, width):
        self.width = float(width)
        self.scale()

    def set_height(self, height):
        self.height = float(height)
        self.scale()

    def scale(self):
        self.font = self.system.font.get_font(self.font_size)

        window_width = self.system.window.get_width()
        window_height = self.system.window.get_height()

        width = max(1, int(window_width * self.width))
        height = max(1, int(window_height * self.height))
        option_height = self.font.get_height() + 2

        x, y = self.get_screen_position()

        self.rect = self.system.window.make_surface(width, height).get_rect(midtop=(x, y - height // 2))
        self.select_rect = self.rect.copy()

        visible_count = min(self.max_visible_options, len(self.options))
        total_height = height

        if self.is_open:
            total_height += visible_count * option_height

        self.surface = self.system.window.make_surface(width, total_height)
        self.option_rects = []

        if not self.is_open:
            return

        for index in range(visible_count):
            rect = self.rect.copy()
            rect.x = self.rect.x
            rect.y = self.rect.bottom + index * option_height
            rect.width = width
            rect.height = option_height
            self.option_rects.append(rect)

    def handle_event(self, event):
        if event.type == self.system.input.video_resize_event():
            self.scale()
            return

        if not self.is_active:
            return

        if event.type == self.system.input.mouse_scroll_event():
            if not self.is_open:
                return

            max_offset = max(0, len(self.options) - self.max_visible_options)
            self.scroll_offset -= event.y
            self.scroll_offset = max(0, min(self.scroll_offset, max_offset))
            self.scale()
            return

        if event.type != self.system.input.mouse_button_down():
            return

        if event.button != 1:
            return

        mouse_pos = self.system.input.get_mouse_pos()

        if self.select_rect.collidepoint(mouse_pos):
            self.is_open = not self.is_open
            self.scale()
            return

        if not self.is_open:
            return

        for index, rect in enumerate(self.option_rects):
            if not rect.collidepoint(mouse_pos):
                continue

            option_index = self.scroll_offset + index

            if option_index >= len(self.options):
                return

            self.selected_option = self.options[option_index]
            self.normalize_boolean_options()
            self.is_open = False
            self.scroll_offset = 0
            self.scale()
            return

        self.is_open = False
        self.scale()

    def get_return_string(self):
        if self.selected_option is None:
            return ""

        return str(self.selected_option)

    def get_selected(self):
        return self.selected_option

    def update(self):
        pass

    def draw(self):
        if self.surface is None:
            return

        self.surface.fill(self.background_color)

        select_surface_rect = self.select_rect.copy()
        select_surface_rect.x -= self.rect.x
        select_surface_rect.y -= self.rect.y

        self.system.window.draw_rect(self.surface, black, select_surface_rect, 2)

        if self.selected_option is not None:
            surf = self.font.render(str(self.selected_option), False, black)
            text_rect = surf.get_rect(midleft=(self.padding, select_surface_rect.centery))
            self.surface.blit(surf, text_rect)

        arrow_x = select_surface_rect.right - 20
        arrow_y = select_surface_rect.centery

        self.system.window.draw_polygon(self.surface, black, [(arrow_x - 7, arrow_y - 3), (arrow_x + 7, arrow_y - 3), (arrow_x, arrow_y + 5)])

        if self.is_open:
            mouse_pos = self.system.input.get_mouse_pos()

            visible_options = self.options[self.scroll_offset:self.scroll_offset + self.max_visible_options]

            for index, option in enumerate(visible_options):
                if index >= len(self.option_rects):
                    break

                dropdown_rect = self.option_rects[index]
                rect = dropdown_rect.copy()
                rect.x -= self.rect.x
                rect.y -= self.rect.y

                option_background = (220, 220, 220) if dropdown_rect.collidepoint(mouse_pos) else white
                self.surface.fill(option_background, rect)

                surf = self.font.render(str(option), False, black)
                text_rect = surf.get_rect(midleft=(self.padding, rect.centery))
                self.surface.blit(surf, text_rect)

                self.system.window.draw_rect(self.surface, black, rect, 1)

        self.system.window.blit(self.surface, self.rect)