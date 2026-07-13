import os

class MenuManager:
    def __init__(self, system):
        self.system = system
        self.menus = {}

    def load(self):
        menu_dir = "enginepersistence/menus"

        if not os.path.exists(menu_dir):
            return

        for file in os.listdir(menu_dir):
            if file.endswith(".menu"):
                self.load_menu(os.path.join(menu_dir, file))

    def get(self, name):
        return self.menus[name]