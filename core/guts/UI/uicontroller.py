class UIController:
    def __init__(self, system, loader):
        self.system = system
        self.loader = loader
        self.active_ui = None
        self.active_name = None

    def show_ui(self, name):
        ui_file = self.system.persistence.get_menu(name)
        if not ui_file.exists():
            ui_file = self.system.persistence.get_form(name)
            if not ui_file.exists():
                self.clear()
                return False

        self.active_ui = self.active_ui, self.active_name, self.active_type = self.loader.load(ui_file)
        self.active_name = name
        return True

    def clear(self):
        self.active_ui = None
        self.active_name = None

    def reload(self):
        if self.active_name:
            self.show_ui(self.active_name)

    def handle_event(self, event):
        if self.active_ui:
            self.active_ui.handle_event(event)

    def update(self):
        if self.active_ui:
            self.active_ui.update()

    def draw(self):
        if self.active_ui:
            self.active_ui.draw()

    def scale(self):
        if self.active_ui:
            self.active_ui.scale()

    def get_active_ui(self):
        return self.active_ui