from core.ui.type import WIDGET
from core.ui.element import UIElement
from core.ui.font import FontEngine
from core.util.colors import red,white,black

class TextBox(UIElement):
    def __init__(self,system,id,position,is_active=False):
        super().__init__(focusable=True,position=position)
        self.system = system
        self.id = id
        self.font = FontEngine(30).font
        self.background_color = black
        self.scale()
        self.string = None
        self.box = []
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

    def handle_event(self, event):
        if self.is_active:
            key = self.system.input.handle_event(event, True)
            if key is not None:
                self.add_key_to_box(key)

                if event.key == self.system.input.keys.backspace_key():
                    if len(self.box) > 0:
                        self.delete_key()

        if event.type == self.system.input.video_resize_event():
            self.scale()

    def set_active(self, state):
        self.is_active = state
        self.cursor_visible = True
        self.cursor_timer = self.system.time.get_current_time()

    def draw_cursor(self):
        if self.is_active:
            now = self.system.time.get_current_time()

            if now - self.cursor_timer  >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = now
            return self.cursor if self.cursor_visible else ""

    def scale(self):
        x,y = self.get_screen_position()

        self.bounding_box = self.system.window.make_surface(275, 100)
        self.bounding_box_rect = self.bounding_box.get_rect(
            center=(x, y)
        )

        self.bounding_box.fill((self.background_color))

        self.text_box = self.system.window.make_surface(250,50)
        self.text_box_rect = self.text_box.get_rect(
            center=self.bounding_box_rect.center
        )

        self.text_box.fill(white)

    def add_key_to_box(self,key):
        if len(self.box) < 21:
            current_key = self.system.input.get_key_name(key)
            allowed_keys = "asdfghjklzxcvbnmqwertyuiopASDFGHJKLZXCVBNMQWERTYUIOP123456789"

            if current_key in allowed_keys:
                self.box.append(current_key)

            if current_key == 'space':
                self.box.append(" ")

            self.cursor_visible = True
            self.cursor_timer = self.system.time.get_current_time()
    
    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        if len(self.box) > 0:
            self.box.pop(-1)

    def update(self):
        pass

    def draw(self):
        if self.is_password:
            text = "*" * len(self.box)
        else:
            text = ''.join(self.box)

        surf = self.font.render(text, False, black)
        rect = surf.get_rect(center=self.text_box_rect.center)
        self.bounding_box.fill((self.background_color))
        self.system.window.blit(self.bounding_box,self.bounding_box_rect)
        self.system.window.blit(self.text_box,self.text_box_rect)
        self.system.window.blit(surf,rect)

        if self.draw_cursor():
            cursor_surf = self.font.render("|", False, black)
            cursor_rect = cursor_surf.get_rect()
            cursor_rect.midleft = (rect.right, rect.centery)
            self.system.window.blit(cursor_surf, cursor_rect)