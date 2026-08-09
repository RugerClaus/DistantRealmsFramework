from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import white


class ScrollableText(UIElement):

    def __init__(
        self,
        system,
        id,
        font_size=40,
        position=(0.5, 0.5),
        width=0.8,
        height=0.6,
        align="left",
        line_spacing=0.01,
        source=None
    ):
        super().__init__(position=position)

        self.system = system
        self.id = id
        self.type = WIDGET.SCROLLABLETEXT

        self.font_size = font_size
        self.font = FontEngine(font_size).font

        self.position = tuple(position)
        self.x_ratio, self.y_ratio = self.position

        self.width = width
        self.height = height

        self.align = align
        self.line_spacing = line_spacing

        self.max_char_count = 90

        self.lines = []
        self.scroll_offset = 0

        self.show_scrollbar = True
        self.scrollbar_width = 6
        self.scrollbar_color = (120, 120, 120)
        self.scrollbar_track_color = (40, 40, 40)

        self.surface = None
        self.rect = None

        self.scale()

        if source:
            self.load_source(source)

    
    def load_source(self, filename):
        from pathlib import Path
        import sys

        try:
            if getattr(sys, "frozen", False):
                base_dir = Path(sys.executable).parent
            else:
                base_dir = Path(__file__).resolve().parent

            filepath = base_dir / filename

            with open(filepath, "r", encoding="utf-8") as file:
                lines = [
                    line.rstrip("\n")
                    for line in file
                ]

            self.set_text(
                self.wrap_lines(lines)
            )

        except FileNotFoundError:
            self.set_text([
                [
                    (
                        "Unable to load text.",
                        0.05,
                        white
                    )
                ]
            ])

    def wrap_lines(self, lines):
        wrapped = []

        for line in lines:
            if not line.strip():
                wrapped.append([])
                continue

            words = line.split()
            current_line = ""

            for word in words:
                if (
                    len(current_line)
                    + len(word)
                    + 1
                    > self.max_char_count
                ):
                    if current_line:
                        wrapped.append([
                            (
                                current_line,
                                0.05,
                                white
                            )
                        ])

                    current_line = word

                else:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word

            if current_line:
                wrapped.append([
                    (
                        current_line,
                        0.05,
                        white
                    )
                ])

        return wrapped

    def set_text(self, text):
        self.lines = text
        self.scroll_offset = 0

    def set_position(self, position):
        self.position = tuple(position)
        self.x_ratio, self.y_ratio = self.position
        super().set_position(self.position)
        self.scale()

    def set_width(self, width):
        self.width = float(width)
        self.scale()

    def set_height(self, height):
        self.height = float(height)
        self.scale()

    def set_align(self, align):
        self.align = align

    def set_line_spacing(self, spacing):
        self.line_spacing = float(spacing)

    def scale(self):
        screen_width = self.system.window.get_width()
        screen_height = self.system.window.get_height()

        width = max(
            1,
            int(screen_width * self.width)
        )

        height = max(
            1,
            int(screen_height * self.height)
        )

        self.surface = self.system.window.make_surface(
            width,
            height,
            True
        )

        x, y = self.get_screen_position()

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def get_rect(self):
        return self.rect

    def visible_lines(self):
        if self.surface is None:
            return 1

        line_height = self.font.get_height()

        spacing = int(
            self.system.window.get_height()
            * self.line_spacing
        )

        return max(
            1,
            self.surface.get_height()
            // (line_height + spacing)
        )

    def scroll(self, amount):
        visible = self.visible_lines()

        max_scroll = max(
            0,
            len(self.lines) - visible
        )

        self.scroll_offset = max(
            0,
            min(
                max_scroll,
                self.scroll_offset + amount
            )
        )

    def handle_event(self, event):
        if event.type == self.system.input.mouse_scroll_event():
            self.scroll(-event.y)

    def resolve_color(self, color):
        if callable(color):
            return color()

        return color

    def draw(self):
        if self.surface is None:
            return

        self.surface.fill((0, 0, 0, 0))

        line_height = self.font.get_height()

        spacing = int(
            self.system.window.get_height()
            * self.line_spacing
        )

        visible_count = self.visible_lines()

        visible = self.lines[
            self.scroll_offset:
            self.scroll_offset + visible_count
        ]

        for index, columns in enumerate(visible):

            draw_y = (
                line_height // 2
                + index * (line_height + spacing)
            )

            for text, normalized_x, color in columns:

                color = self.resolve_color(color)

                text_surface = self.font.render(
                    text,
                    True,
                    color
                )

                x = int(
                    normalized_x
                    * self.surface.get_width()
                )

                if self.align == "center":

                    text_rect = text_surface.get_rect(
                        center=(x, draw_y)
                    )

                elif self.align == "right":

                    text_rect = text_surface.get_rect(
                        right=x,
                        centery=draw_y
                    )

                else:

                    text_rect = text_surface.get_rect(
                        left=x,
                        centery=draw_y
                    )

                self.surface.blit(
                    text_surface,
                    text_rect
                )

        if self.show_scrollbar:
            self.draw_scrollbar()

        self.system.window.blit(
            self.surface,
            self.rect
        )

    def draw_scrollbar(self):
        total = len(self.lines)
        visible = self.visible_lines()

        if total <= visible:
            return

        scrollbar_height = self.surface.get_height()

        scrollbar_x = (
            self.surface.get_width()
            - self.scrollbar_width
        )

        track = self.system.window.make_surface(
            self.scrollbar_width,
            scrollbar_height,
            True
        )

        track.fill(
            self.scrollbar_track_color
        )

        self.surface.blit(
            track,
            (
                scrollbar_x,
                0
            )
        )

        ratio = visible / total

        handle_height = max(
            20,
            int(scrollbar_height * ratio)
        )

        max_handle_y = (
            scrollbar_height
            - handle_height
        )

        max_scroll = total - visible

        if max_scroll > 0:
            scroll_ratio = (
                self.scroll_offset
                / max_scroll
            )
        else:
            scroll_ratio = 0

        handle_y = int(
            max_handle_y
            * scroll_ratio
        )

        handle = self.system.window.make_surface(
            self.scrollbar_width,
            handle_height,
            True
        )

        handle.fill(
            self.scrollbar_color
        )

        self.surface.blit(
            handle,
            (
                scrollbar_x,
                handle_y
            )
        )

    def update(self):
        pass