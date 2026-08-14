from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import red, white, black


class TextBox(UIElement):

    def __init__(
        self,
        system,
        id,
        position,
        dimensions=(0.1432, 0.0926),
        font_size=30,
        is_active=False,
        is_password=False,
        text=None,
        char_limit=21
    ):
        super().__init__(focusable=True, position=position)

        self.system = system
        self.id = id

        self.font = FontEngine(font_size).font

        self.background_color = black

        self.width, self.height = dimensions

        self.text_width = 0.9091
        self.text_height = 0.5

        # Maximum number of characters allowed.
        self.limit = char_limit

        self.scale()

        # Always enforce the character limit when initial text is loaded.
        initial_text = "" if text is None else str(text)

        if self.limit is not None:
            initial_text = initial_text[:self.limit]

        self.box = list(initial_text)

        self.is_password = is_password

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
        text = str(text)

        if self.limit is not None:
            text = text[:self.limit]

        self.box = list(text)

        # Make sure the cursor immediately appears at the end.
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

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

        return ""

    def scale(self):
        x, y = self.get_screen_position()

        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

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
        # Do NOT use textbox width to determine the character limit.
        # The character limit is purely based on self.limit.
        if self.limit is not None and len(self.box) >= self.limit:
            return

        self.box.append(character)

        # Reset cursor blink when text changes.
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        if self.box:
            self.box.pop()

        # Reset cursor blink when text changes.
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

    def update(self):
        pass

    def _get_visible_text(self, text, available_width):
        """
        Return the portion of text that can currently be displayed.

        The END of the text is always kept visible. This means that when
        the text becomes wider than the textbox, the textbox effectively
        scrolls horizontally toward the right.
        """

        if not text:
            return ""

        # If the entire string fits, show everything.
        full_surface = self.font.render(text, False, black)

        if full_surface.get_width() <= available_width:
            return text

        # Build the visible string from the end until it no longer fits.
        visible = ""

        for character in reversed(text):
            candidate = character + visible

            candidate_surface = self.font.render(
                candidate,
                False,
                black
            )

            if candidate_surface.get_width() > available_width:
                break

            visible = candidate

        return visible

    def draw(self):
        if self.is_password:
            text = "*" * len(self.box)
        else:
            text = ''.join(self.box)

        self.bounding_box.fill(self.background_color)

        self.system.window.blit(
            self.bounding_box,
            self.bounding_box_rect
        )

        self.system.window.blit(
            self.text_box,
            self.text_box_rect
        )

        # Leave enough room for the cursor when active.
        cursor_surf = None

        if self.is_active:
            cursor_surf = self.font.render(
                "|",
                False,
                black
            )

            cursor_width = cursor_surf.get_width()
        else:
            cursor_width = 0

        available_width = self.text_box.get_width()

        if self.is_active:
            available_width -= cursor_width

        available_width = max(1, available_width)

        # Only the visible portion is selected here.
        # The actual self.box remains untouched.
        visible_text = self._get_visible_text(
            text,
            available_width
        )

        surf = self.font.render(
            visible_text,
            False,
            black
        )

        # Position the visible text so its RIGHT edge is immediately
        # before the cursor. This keeps the end of the text visible.
        if self.is_active:
            text_right = (
                self.text_box_rect.right
                - cursor_width
            )

            rect = surf.get_rect(
                midright=(
                    text_right,
                    self.text_box_rect.centery
                )
            )
        else:
            rect = surf.get_rect(
                center=self.text_box_rect.center
            )

        self.system.window.blit(
            surf,
            rect
        )

        # Cursor always follows the END of the visible text.
        if self.draw_cursor():
            cursor_rect = cursor_surf.get_rect(
                midleft=(
                    rect.right,
                    rect.centery
                )
            )

            self.system.window.blit(
                cursor_surf,
                cursor_rect
            )