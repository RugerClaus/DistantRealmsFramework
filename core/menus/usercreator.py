from core.ui.textbox import TextBox
from core.network.user import User

class UserCreator:
    def __init__(self,system):
        self.system = system
        self.text_box = TextBox(system)
        self.user = User(system)
    
    def handle_event(self,event):
        self.text_box.handle_event(event)

    def scale(self):
        self.text_box.scale()

    def draw(self):
        self.text_box.draw()
    
    def submit(self):
        username = self.text_box.get_return_string()
        if username is not None:
            self.system.save.write_constant('username',str(username))
            self.text_box.box.clear()