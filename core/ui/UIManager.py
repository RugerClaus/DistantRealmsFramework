from core.ui.type import WIDGET
class UIManager:
    def __init__(self,system):
        self.system = system
        self.elements = []
        self.active_element = None

    def add(self, element):
        self.elements.append(element)

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()

            if (self.active_element and self.active_element.type == WIDGET.SELECT and self.active_element.is_open):
                self.active_element.handle_event(event)
                return

            for element in self.elements:
                if element.focusable:
                    if element.contains_point(mouse_pos):
                        self.set_active(element)
                        break

            for element in self.elements:
                if element.type == WIDGET.BUTTON:
                    if element.is_clicked(mouse_pos, True):
                        break

        if self.active_element:
            self.active_element.handle_event(event)

        if event.type == self.system.input.keydown():
            if event.key == self.system.input.keys.tab_key():
                focusable_elements = [element for element in self.elements if element.focusable]

                if not focusable_elements:
                    return

                if self.active_element in focusable_elements:
                    index = focusable_elements.index(self.active_element)
                    next_index = (index + 1) % len(focusable_elements)
                else:
                    next_index = 0

                self.set_active(focusable_elements[next_index])

        for element in self.elements:
            if element.type == WIDGET.SCROLLABLETEXT:
                element.handle_event(event)


    def set_active(self, element):
        if self.active_element:
            self.active_element.set_active(False)

        self.active_element = element
        element.set_active(True)

    def update(self):
        mouse_pos = self.system.input.get_mouse_pos()
        for element in self.elements:
            if element.type == WIDGET.BUTTON:
                element.update(mouse_pos)

    def draw(self):
        for element in self.elements:
            element.draw()

    def scale(self):
        for element in self.elements:
            element.scale()