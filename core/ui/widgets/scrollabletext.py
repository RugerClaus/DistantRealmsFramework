from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.util.colors import white


class ScrollableText(UIElement):
    def __init__(self,system,id,font_size=40,position=(0.5,0.5),width=0.8,height=0.6,align="left",line_spacing=0.01,source=None,vertical_align="top",direction="down"):
        super().__init__(position=position,focusable=True)
        self.system=system
        self.id=id
        self.type=WIDGET.SCROLLABLETEXT
        self.font_size=font_size
        self.position=tuple(position)
        self.x_ratio,self.y_ratio=self.position
        self.width=width
        self.height=height
        self.align=align
        self.vertical_align=vertical_align
        self.direction=direction
        self.line_spacing=line_spacing
        self.max_char_count=90
        self.lines=[]
        self.scroll_offset=0
        self.show_scrollbar=True
        self.scrollbar_width=6
        self.scrollbar_color=(120,120,120)
        self.scrollbar_track_color=(40,40,40)
        self.surface=None
        self.rect=None
        self.scale()

        self.fade_duration=2000
        self.fade_start=None
        self.fading=False
        self.alpha=255

        if source:
            self.load_source(source)

    def fade_out(self,duration=2000):
        self.fade_duration=duration
        self.fade_start=self.system.time.get_current_time()
        self.fading=True
        self.alpha=255

    def load_source(self,filename):
        from helper import asset
        from pathlib import Path

        try:
            filepath=Path(filename)

            if not filepath.exists():
                filepath=Path(asset(filename))

            with filepath.open("r",encoding="utf-8") as file:
                lines=[
                    line.rstrip("\n")
                    for line in file
                ]

            self.set_text(self.wrap_lines(lines))

        except (FileNotFoundError,TypeError):
            self.set_text([[("Unable to load text.",0.05,white)]])

    def wrap_lines(self, lines):
        wrapped = []

        for line in lines:
            if not line.strip():
                wrapped.append([])
                continue

            words = line.split()
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 > self.max_char_count:
                    if current_line:
                        wrapped.append([(current_line,0.05,white)])

                    current_line = word

                else:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word

            if current_line:
                wrapped.append([(current_line,0.05,white)])

        return wrapped

    def set_text(self,text):
        self.lines=text

        if self.direction=="down":
            visible=self.visible_lines()
            self.scroll_offset=max(0,len(self.lines)-visible)
        else:
            self.scroll_offset=0

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
        self.font = self.system.font.get_font(self.font_size)
        screen_width = self.system.window.get_width()
        screen_height = self.system.window.get_height()

        width = max(1,int(screen_width * self.width))

        height = max(1,int(screen_height * self.height))

        self.surface = self.system.window.make_surface(width,height,True)

        x, y = self.get_screen_position()

        self.rect = self.surface.get_rect(center=(x, y))

    def get_rect(self):
        return self.rect

    def visible_lines(self):
        if self.surface is None:
            return 1

        line_height = self.font.get_height()

        spacing = int(self.system.window.get_height() * self.line_spacing)

        return max(1,self.surface.get_height() // (line_height + spacing))

    def scroll(self,amount):
        visible=self.visible_lines()
        max_scroll=max(0,len(self.lines)-visible)

        old=self.scroll_offset
        self.scroll_offset=max(0,min(max_scroll,self.scroll_offset+amount))

    def handle_event(self,event):
        if event.type == self.system.input.mouse_scroll_event():
            self.scroll(-event.y)

    def resolve_color(self, color):
        if callable(color):
            return color()

        return color

    def apply_alpha(self):
        if self.alpha>=255:
            return

        self.surface.fill(
            (255,255,255,self.alpha),
            special_flags=self.system.backend.pygame.BLEND_RGBA_MULT
        )

    def draw(self):
        if self.surface is None:
            return

        self.surface.fill((0,0,0,0))

        line_height=self.font.get_height()
        spacing=int(self.system.window.get_height()*self.line_spacing)
        step=line_height+spacing
        visible_count=self.visible_lines()
        max_scroll=max(0,len(self.lines)-visible_count)

        if self.direction=="up":
            start=max(0,len(self.lines)-visible_count-self.scroll_offset)
            visible=self.lines[start:start+visible_count]
        else:
            start=self.scroll_offset
            visible=self.lines[start:start+visible_count]

        if self.vertical_align=="bottom":
            if self.direction=="up":
                start_y=self.surface.get_height()-line_height//2
            else:
                start_y=self.surface.get_height()-line_height//2-(len(visible)-1)*step
        else:
            if self.direction=="up":
                start_y=line_height//2+(len(visible)-1)*step
            else:
                start_y=line_height//2

        for index,columns in enumerate(visible):
            if self.direction=="up":
                draw_y=start_y-index*step
            else:
                draw_y=start_y+index*step

            for text,normalized_x,color in columns:
                color=self.resolve_color(color)

                if len(color)==4:
                    color=(*color[:3],self.alpha)
                else:
                    color=(*color,self.alpha)

                text_surface=self.font.render(text,True,color)
                x=int(normalized_x*self.surface.get_width())

                if self.align=="center":
                    text_rect=text_surface.get_rect(center=(x,draw_y))
                elif self.align=="right":
                    text_rect=text_surface.get_rect(right=x,centery=draw_y)
                else:
                    text_rect=text_surface.get_rect(left=x,centery=draw_y)

                self.surface.blit(text_surface,text_rect)

        if self.show_scrollbar:
            self.draw_scrollbar()

        if self.fading:
            self.apply_alpha()

        self.system.window.mark_surface_dirty(self.surface)
        self.system.window.blit(self.surface,self.rect)

        if self.fading:
            self.alpha=255

    def draw_scrollbar(self):
        total = len(self.lines)
        visible = self.visible_lines()

        if total <= visible:
            return

        scrollbar_height = self.surface.get_height()

        scrollbar_x = self.surface.get_width() - self.scrollbar_width

        track = self.system.window.make_surface(self.scrollbar_width,scrollbar_height,True)

        track.fill(self.scrollbar_track_color)

        self.surface.blit(track,(scrollbar_x,0))

        ratio = visible / total

        handle_height = max(20,int(scrollbar_height * ratio))

        max_handle_y = (scrollbar_height - handle_height)

        max_scroll = total - visible

        if max_scroll > 0:
            scroll_ratio = (self.scroll_offset / max_scroll)
        else:
            scroll_ratio = 0

        handle_y = int(max_handle_y * scroll_ratio)

        handle = self.system.window.make_surface(self.scrollbar_width,handle_height,True)

        handle.fill(self.scrollbar_color)

        self.surface.blit(handle,(scrollbar_x,handle_y))

    def update(self):
        if not self.fading:
            return

        now=self.system.time.get_current_time()
        elapsed=now-self.fade_start

        if elapsed>=self.fade_duration:
            self.alpha=0
            self.fading=False
            return

        self.alpha=max(0,int(255*(1-(elapsed/self.fade_duration))))