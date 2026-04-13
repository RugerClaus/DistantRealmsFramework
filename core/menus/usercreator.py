from core.ui.textbox import TextBox
from helper import *

class UserCreator:
    def __init__(self,system):
        self.system = system
        self.text_box = TextBox(system)
    
    def handle_event(self,event):
        self.text_box.handle_event(event)

    def scale(self):
        self.text_box.scale()

    def draw(self):
        self.text_box.draw()
    
    def submit(self):
        username = self.text_box.get_return_string()
        if username is not None:
            write_constant_to_file('username',str(username))
            self.text_box.box.clear()