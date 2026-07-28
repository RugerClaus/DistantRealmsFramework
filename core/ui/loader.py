import json
from systemlogging import log_error

from core.ui.composables.form import Form
from core.ui.composables.menu import Menu
from core.ui.widgets.label import Label
from core.ui.widgets.query import Query
from core.ui.widgets.textbox import TextBox
from core.ui.widgets.button import Button
from core.ui.widgets.image import Image
from core.ui.widgets.scrollabletext import ScrollableText
from core.ui.widgets.centertext import CenterText

class UILoader:
    def __init__(self, system, actions):
        self.system = system
        self.actions = actions

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        if data["type"] == "form":
            return self.load_form(data)
        elif data["type"] == "menu":
            return self.load_menu(data)

        raise ValueError(f"Unknown UI type: {data['type']}")

    def load_menu(self, data):
        menu = Menu(self.system)

        for element_data in data["elements"]:
            element = self.create_element(element_data)
            menu.add_child(element)

        menu.on_load()
        return menu

    def load_form(self, data):
        form = Form(self.system)
        elements = {}

        for definition in data.get("elements", []):
            element = self.create_element(definition)
            elements[definition["id"]] = element

            if "field" in definition:
                form.add_field(definition["field"], element)
            else:
                form.add_child(element)

        if "error_element" in data:
            form.set_error_element(elements[data["error_element"]])

        return form

    def create_element(self, data):
        element_type = data["type"]
        element_id = data.get("id")

        if element_type == "label":
            return Label(self.system, element_id, data.get("text", ""), tuple(data.get("position", [0, 0])))

        elif element_type == "textbox":
            element = TextBox(self.system, element_id, tuple(data.get("position", [0, 0])))

            if data.get("password", False):
                element.is_password = True

            return element

        elif element_type == "button":
            action = data.get("action")
            callback = self.actions.execute if action else None
            return Button(self.system, element_id, data.get("font_size", 40), data.get("text", ""), tuple(data.get("position", [0, 0])), lambda: callback(action) if callback else None)

        elif element_type == "query":
            return Query(self.system, element_id, data.get("text", ""))

        elif element_type == "image":
            return Image(self.system, element_id, data.get("asset"), tuple(data.get("position", [0.5, 0.5])), data.get("scale", [1.0, 1.0]))

        elif element_type == "scrollable_text":
            element = ScrollableText(
                self.system,
                element_id,
                font_size=data.get("font_size", 40),
                anchor=tuple(data.get("position", [0.5, 0.5])),
                width=data.get("width", 0.8),
                height=data.get("height", 0.6),
                align=data.get("align", "left"),
                line_spacing=data.get("line_spacing", 0.01)
            )
            element.load_source(data.get("text"))
            return element

        elif element_type == "center_text":
            return CenterText(
                self.system,
                element_id,
                font_size=data.get("font_size", 40),
                position=tuple(data.get("position", [0.5, 0.5])),
                text=data.get("text", "")
            )

        log_error(f"Unknown UI element type: {element_type}")