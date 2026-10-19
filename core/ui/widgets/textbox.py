from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.util.colors import red, white, black


class TextBox(UIElement):

    def __init__(self,system,id,position,dimensions=(0.1432,0.0926),font_size=30,is_active=False,is_password=False,text=None,char_limit=21):
        super().__init__(focusable=True,position=position)

        self.system = system
        self.id = id
        self.font_size = font_size

        self.background_color = white
        self.text_color = black
        self.border_color = black
        self.border_width = 2

        self.width,self.height = dimensions

        self.text_width = 0.9091
        self.text_height = 0.5

        self.limit = char_limit

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

        self.font = None
        self.cursor_surf = None
        self.text_surf = None
        self.rendered_text = None
        self.rendered_available_width = None

        self.bounding_box = None
        self.text_box = None
        self.bounding_box_rect = None
        self.text_box_rect = None

        self.scale()

    def set_background_color(self,color):
        self.background_color = color
        self.scale()

    def set_text_color(self,color):
        self.text_color = color

        if self.font is not None:
            self.cursor_surf = self.font.render("|",False,self.text_color)

        self.rendered_text = None
        self._update_text_surface()

    def set_border_color(self,color):
        self.border_color = color
        self.scale()

    def set_border_width(self,width):
        self.border_width = max(0,int(width))
        self.scale()

    def error_back(self):
        self.set_border_color(red)

    def clear_error(self):
        self.set_border_color(black)

    def set_text(self,text):
        text = str(text)

        if self.limit is not None:
            text = text[:self.limit]

        self.box = list(text)

        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

        self._update_text_surface()

    def handle_event(self,event):
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

    def contains_point(self,position):
        return self.bounding_box_rect.collidepoint(position)

    def set_active(self,state):
        self.is_active = state
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()
        self._update_text_surface()

    def draw_cursor(self):
        if self.is_active:
            now = self.system.time.get_current_time()

            if now - self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = now

            return self.cursor if self.cursor_visible else ""

        return ""

    def scale(self):
        x,y = self.get_screen_position()

        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        width = int(ww * self.width)
        height = int(wh * self.height)

        self.bounding_box = self.system.window.make_surface(width,height,True)
        self.bounding_box_rect = self.bounding_box.get_rect(center=(x,y))

        self.bounding_box.fill(self.border_color)

        text_width = max(1,width - self.border_width * 2)
        text_height = max(1,height - self.border_width * 2)

        self.text_box = self.system.window.make_surface(text_width,text_height,True)
        self.text_box_rect = self.text_box.get_rect(center=self.bounding_box_rect.center)

        self.text_box.fill(self.background_color)

        self.font = self.system.font.get_font(self.font_size)
        self.cursor_surf = self.font.render("|",False,self.text_color)

        self.rendered_text = None
        self.rendered_available_width = None

        self._update_text_surface()

    def add_key_to_box(self,character):
        if self.limit is not None and len(self.box) >= self.limit:
            return

        self.box.append(character)

        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

        self._update_text_surface()

    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        if self.box:
            self.box.pop()

        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

        self._update_text_surface()

    def update(self):
        pass

    def _get_visible_text(self,text,available_width,font):
        if not text:
            return ""

        full_surface = font.render(text,False,self.text_color)

        if full_surface.get_width() <= available_width:
            return text

        visible = ""

        for character in reversed(text):
            candidate = character + visible
            candidate_surface = font.render(candidate,False,self.text_color)

            if candidate_surface.get_width() > available_width:
                break

            visible = candidate

        return visible

    def _update_text_surface(self):
        if self.font is None or self.text_box is None:
            return

        if self.is_password:
            text = "*" * len(self.box)
        else:
            text = ''.join(self.box)

        cursor_width = self.cursor_surf.get_width() if self.is_active else 0
        available_width = self.text_box.get_width()

        if self.is_active:
            available_width -= cursor_width

        available_width = max(1,available_width)

        visible_text = self._get_visible_text(text,available_width,self.font)

        if visible_text == self.rendered_text and available_width == self.rendered_available_width:
            return

        self.text_surf = self.font.render(visible_text,False,self.text_color)
        self.rendered_text = visible_text
        self.rendered_available_width = available_width

    def draw(self):
        self.bounding_box.fill(self.border_color)

        self.system.window.blit(self.bounding_box,self.bounding_box_rect)
        self.system.window.blit(self.text_box,self.text_box_rect)

        self._update_text_surface()

        if self.is_active:
            text_left = self.text_box_rect.left + self.cursor_surf.get_width()
            rect = self.text_surf.get_rect(midleft=(text_left,self.text_box_rect.centery))
        else:
            rect = self.text_surf.get_rect(center=self.text_box_rect.center)

        self.system.window.blit(self.text_surf,rect)

        if self.draw_cursor():
            cursor_rect = self.cursor_surf.get_rect(midleft=(rect.right,rect.centery))
            self.system.window.blit(self.cursor_surf,cursor_rect)