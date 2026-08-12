from core.ui.element import UIElement
from core.ui.type import COMPOSABLE
from core.ui.UIManager import UIManager


class Menu(UIElement):
    def __init__(self, system):
        super().__init__()

        self.system = system
        self.children = []

        self.ui = UIManager(system)

        self.type = COMPOSABLE.MENU

        self.loaded = False

    def get_element(self, element_id):
        for element in self.children:
            if element.id == element_id:
                return element

        return None

    def add_child(self, element):
        self.children.append(element)
        self.ui.add(element)

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
        pass