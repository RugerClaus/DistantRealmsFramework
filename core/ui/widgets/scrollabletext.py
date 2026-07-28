from core.ui.font import FontEngine
from core.ui.element import UIElement
from core.ui.type import WIDGET

class ScrollableText(UIElement):

    def __init__(
        self,
        system,
        id,
        font_size=40,
        anchor=(0.5, 0.5),
        width=0.8,
        height=0.6,
        align="left",
        line_spacing=0.01,
        source=None
    ):
        super().__init__(position=anchor)
        self.system = system
        self.id = id
        self.type = WIDGET.SCROLLABLETEXT
        self.font = FontEngine(font_size).font

        self.anchor = anchor
        self.width = width
        self.height = height

        self.max_char_count = 90

        self.align = align
        self.line_spacing = line_spacing

        self.lines = []
        self.scroll_offset = 0

        self.surface = None
        self.scale()

        self.show_scrollbar = True
        self.scrollbar_width = 6
        self.scrollbar_color = (120,120,120)
        self.scrollbar_track_color = (40,40,40)
        if source:
            self.load_source(source)

    def load_source(self, filename):
        try:
            with open(filename, "r") as file:
                lines = [line.rstrip("\n") for line in file]

            self.set_text(self.wrap_lines(lines))

        except FileNotFoundError:
            self.set_text([
                [(
                    "Unable to load text.",
                    0.05,
                    (255, 255, 255)
                )]
            ])

    def wrap_lines(self, lines):
        wrapped = []

        for line in lines:
            words = line.split(" ")
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 > self.max_char_count:
                    wrapped.append([
                        (
                            current_line,
                            0.05,
                            (255, 255, 255)
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
                        (255, 255, 255)
                    )
                ])

        return wrapped

    def scale(self):

        width = int(
            self.system.window.get_width()
            * self.width
        )

        height = int(
            self.system.window.get_height()
            * self.height
        )

        self.surface = self.system.window.make_surface(
            width,
            height,
            True
        )


    def normalized_to_pixel(self, x, y):

        return (
            int(x * self.system.window.get_width()),
            int(y * self.system.window.get_height())
        )


    def get_rect(self):

        x, y = self.normalized_to_pixel(
            *self.anchor
        )

        width = int(
            self.system.window.get_width()
            * self.width
        )

        height = int(
            self.system.window.get_height()
            * self.height
        )

        return (
            x,
            y,
            width,
            height
        )


    def set_text(self, text):

        self.lines = text

        self.scroll_offset = 0

    def handle_event(self, event):
        if event.type == self.system.input.mouse_scroll_event():
            self.scroll(-event.y)

    def scroll(self, amount):

        max_scroll = max(
            0,
            len(self.lines) - self.visible_lines()
        )

        self.scroll_offset = max(
            0,
            min(
                max_scroll,
                self.scroll_offset + amount
            )
        )


    def visible_lines(self):

        _, _, _, height = self.get_rect()

        line_height = self.font.get_height()

        spacing = int(
            self.system.window.get_height()
            * self.line_spacing
        )

        return max(
            1,
            height // (line_height + spacing)
        )


    def resolve_color(self, color):

        if callable(color):
            return color()

        return color


    def draw(self):

        x, y = self.normalized_to_pixel(
            *self.anchor
        )

        self.surface.fill(
            (0, 0, 0, 0)
        )


        line_height = self.font.get_height()

        spacing = int(
            self.system.window.get_height()
            * self.line_spacing
        )


        visible = self.lines[
            self.scroll_offset:
            self.scroll_offset + self.visible_lines()
        ]


        for index, columns in enumerate(visible):

            draw_y = (
                line_height // 2
                +
                index * (
                    line_height + spacing
                )
            )


            for text, normalized_x, color in columns:

                color = self.resolve_color(color)

                surf = self.font.render(
                    text,
                    True,
                    color
                )


                x_pos, _ = self.normalized_to_pixel(
                    normalized_x,
                    0
                )


                relative_x = (
                    x_pos
                    -
                    self.normalized_to_pixel(
                        self.anchor[0],
                        0
                    )[0]
                )


                if self.align == "center":

                    rect = surf.get_rect(
                        center=(
                            relative_x,
                            draw_y
                        )
                    )

                elif self.align == "right":

                    rect = surf.get_rect(
                        right=relative_x,
                        centery=draw_y
                    )

                else:

                    rect = surf.get_rect(
                        left=relative_x,
                        centery=draw_y
                    )


                self.surface.blit(
                    surf,
                    rect
                )

        if self.show_scrollbar:
            self.draw_scrollbar()

        self.system.window.blit(
            self.surface,
            (x, y)
        )
        
    def draw_scrollbar(self):

        total = len(self.lines)
        visible = self.visible_lines()

        if total <= visible:
            return


        scrollbar_height = self.surface.get_height() -50

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
                self.surface.get_width()
                - self.scrollbar_width,
                0
            )
        )


        ratio = visible / total

        handle_height = max(
            20,
            int(
                scrollbar_height * ratio
            )
        )


        scroll_ratio = (
            self.scroll_offset
            /
            (total - visible)
        )


        handle_y = int(
            (
                scrollbar_height
                -
                handle_height
            )
            *
            scroll_ratio
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
                self.surface.get_width()
                - self.scrollbar_width,
                handle_y
            )
        )