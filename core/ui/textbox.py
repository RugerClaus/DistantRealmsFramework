from core.ui.font import FontEngine

from helper import *

class TextBox:
    def __init__(self,system):
        self.system = system
        self.font = FontEngine(30).font
        self.scale()
        self.string = None
        self.box = [' ']

    def handle_event(self,event):
        key = self.system.input.handle_event(event,True)
        if key is not None:
            self.add_key_to_box(key)
            if self.system.input.get_key_name(key) == 'backspace' and len(self.box) > 0:
                self.delete_key()
        if event.type == self.system.input.video_resize_event():
            self.bounding_box_rect = self.bounding_box.get_rect(center=(self.system.window.get_width()//2,self.system.window.get_height()//3))
            self.text_box_rect.center = self.bounding_box_rect.center

    def scale(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        self.bounding_box = self.system.window.make_surface(275,100)
        self.bounding_box_rect = self.bounding_box.get_rect(center=(ww//2,wh//3))
        self.bounding_box.fill((0,0,0))
        self.text_box = self.system.window.make_surface(250,50)
        self.text_box_rect = self.text_box.get_rect(center=self.bounding_box_rect.center)
        self.text_box.fill((255,255,255))

    def add_key_to_box(self,key):
        if len(self.box) < 21:
            current_key = self.system.input.get_key_name(key)
            allowed_keys = "asdfghjklzxcvbnmqwertyuiopASDFGHJKLZXCVBNMQWERTYUIOP123456789"
            if current_key in allowed_keys:
                self.box.append(self.system.input.get_key_name(key))
            if current_key == 'space':
                self.box.append(" ")
    
    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        self.box.pop(-1)

    def draw(self):
        if len(self.box) > 0:
            text = ''.join(self.box)
        else:
            text = ''
        
        surf = self.font.render(text,False,(0,0,0))
        rect = surf.get_rect(center=self.text_box_rect.center)
        self.system.window.blit(self.bounding_box,self.bounding_box_rect)
        self.system.window.blit(self.text_box,self.text_box_rect)
        self.system.window.blit(surf,rect)