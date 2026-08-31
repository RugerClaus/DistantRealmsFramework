from systemlogging import log_error

from core.ui.element import UIElement
from core.ui.type import COMPOSABLE
from core.ui.UIManager import UIManager


class Form(UIElement):
    def __init__(self, system):
        super().__init__()

        self.system = system
        self.children = []
        self.fields = {}
        self.error_element = None

        self.ui = UIManager(system)

        self.type = COMPOSABLE.FORM
        self.loaded = False

    def get_element(self, element_id):
        for element in self.children:
            if element.id == element_id:
                return element

        return None

    def add_child(self, element):
        self.children.append(element)
        self.ui.add(element)

    def add_field(self, name, element):
        self.fields[name] = element
        self.add_child(element)

    def get_field(self, name):
        if name not in self.fields:
            log_error(f"Form field not found: '{name}'","core.ui.composables.form.Form")
            return None

        return self.fields[name]

    def set_error_element(self, element):
        self.error_element = element
        self.add_child(element)

    def set_error(self, message, color=None):
        if self.error_element:
            self.error_element.text = message

    def clear_error(self):
        if self.error_element:
            self.error_element.text = ""

    def handle_event(self, event):
        self.ui.handle_event(event)

    def on_load(self):
        pass

    def draw(self):
        self.ui.draw()

    def scale(self):
        self.ui.scale()

    def update(self):
        self.ui.update()

    def submit(self):
        return {
            name: element.get_return_string()
            for name, element in self.fields.items()
        }