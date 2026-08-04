from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import red, white, black


class TextBox(UIElement):
    def __init__(self, system, id, position, dimensions=(0.1432,0.0926),font_size=30,is_active=False,text=None):
        super().__init__(focusable=True, position=position)

        self.system = system
        self.id = id

        self.font = FontEngine(font_size).font

        self.background_color = black

        # Normalized dimensions
        self.width, self.height = dimensions

        # Inner text area as a fraction of the textbox
        self.text_width = 0.9091
        self.text_height = 0.5

        self.scale()

        self.box = list(str(text)) if text is not None else []
        self.is_password = False

        self.cursor_interval = 500
        self.cursor = "|"
        self.cursor_timer = self.system.time.get_current_time()
        self.cursor_visible = True

        self.is_active = is_active
        self.type = WIDGET.TEXTBOX
        self.loaded = False

    def error_back(self):
        self.background_color = red

    def clear_error(self):
        self.background_color = black

    def set_text(self, text):
        self.box = list(str(text)[:21])

    def handle_event(self, event):
        if event.type == self.system.input.video_resize_event():
            self.scale()
            return

        if not self.is_active:
            return

        if event.type != self.system.input.keydown():
            return

        if event.key == self.system.input.keys.backspace_key():
            self.delete_key()
            return

        if event.key == self.system.input.keys.enter_key():
            return

        if event.unicode and event.unicode.isprintable():
            self.add_key_to_box(event.unicode)

    def contains_point(self, position):
        return self.bounding_box_rect.collidepoint(position)

    def set_active(self, state):
        self.is_active = state
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

    def draw_cursor(self):
        if self.is_active:
            now = self.system.time.get_current_time()

            if now - self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = now

            return self.cursor if self.cursor_visible else ""

    def scale(self):
        x, y = self.get_screen_position()

        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        # Resolve normalized dimensions into pixels
        width = int(ww * self.width)
        height = int(wh * self.height)

        self.bounding_box = self.system.window.make_surface(
            width,
            height
        )

        self.bounding_box_rect = self.bounding_box.get_rect(
            center=(x, y)
        )

        self.bounding_box.fill(self.background_color)

        # Thin 2-pixel border
        border = 2

        text_width = max(1, width - border * 2)
        text_height = max(1, height - border * 2)

        self.text_box = self.system.window.make_surface(
            text_width,
            text_height
        )

        self.text_box_rect = self.text_box.get_rect(
            center=self.bounding_box_rect.center
        )

        self.text_box.fill(white)

    def add_key_to_box(self, character):
        if len(self.box) >= 21:
            return

        self.box.append(character)
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        if self.box:
            self.box.pop()

    def update(self):
        pass

    def draw(self):
        if self.is_password:
            text = "*" * len(self.box)
        else:
            text = ''.join(self.box)

        surf = self.font.render(text, False, black)
        rect = surf.get_rect(center=self.text_box_rect.center)

        self.bounding_box.fill(self.background_color)

        self.system.window.blit(
            self.bounding_box,
            self.bounding_box_rect
        )

        self.system.window.blit(
            self.text_box,
            self.text_box_rect
        )

        self.system.window.blit(surf, rect)

        if self.draw_cursor():
            cursor_surf = self.font.render("|", False, black)
            cursor_rect = cursor_surf.get_rect()
            cursor_rect.midleft = (rect.right, rect.centery)

            self.system.window.blit(
                cursor_surf,
                cursor_rect
            )