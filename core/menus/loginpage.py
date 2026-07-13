from core.guts.user import User
from core.ui.textbox import TextBox
from core.ui.UIManager import UIManager
from core.ui.label import Label

class LoginPage:
    def __init__(self, system):
        self.system = system
        self.user = User(system)

        self.username_label = Label(system, "Username:", 0.37, 0.3)
        self.username_box = TextBox(system, 0.5, 0.3)

        self.password_label = Label(system, "Password:", 0.37, 0.4)
        self.password_box = TextBox(system, 0.5, 0.4)
        self.password_box.is_password = True

        self.ui = UIManager(system)

        self.ui.add(self.username_label)
        self.ui.add(self.username_box)
        self.ui.add(self.password_label)
        self.ui.add(self.password_box)

        self.ui.set_active(self.username_box)

        self.error = None

    def handle_event(self, event):
        self.ui.handle_event(event)

    def scale(self):
        self.ui.scale()

    def draw(self):
        self.ui.draw()

    def submit(self):
        username = self.username_box.get_return_string()
        password = self.password_box.get_return_string()

        self.error = None

        ehe = (244,20,20)

        if not username:
            self.error = "Username is required"
            return False

        if not password:
            self.error = "Password is required"
            return False

        result = self.system.auth.login(
            username,
            password
        )

        if result["success"]:
            self.username_box.box.clear()
            self.password_box.box.clear()

            self.system.save.write_constant(
                "username",
                username
            )

            return True

        self.error = result["message"]
        return False