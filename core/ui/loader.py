import json
from systemlogging import log_error

from core.ui.composables.form import Form
from core.ui.composables.menu import Menu
from core.ui.widgets.label import Label
from core.ui.widgets.query import Query
from core.ui.widgets.textbox import TextBox
from core.ui.widgets.button import Button
from core.ui.widgets.image import Image
from core.ui.widgets.header import Header
from core.ui.widgets.scrollabletext import ScrollableText
from core.ui.widgets.centertext import CenterText
from core.ui.widgets.select import Select
class UILoader:
    def __init__(self, system, actions):
        self.system = system
        self.actions = actions
        self.menu = None
        self.form = None
        self.current_form = None
        self.current_menu = None

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        if data["type"] == "form":
            return self.load_form(data)
        elif data["type"] == "menu":
            return self.load_menu(data)
        

        raise ValueError(f"Unknown UI type: {data['type']}")

    def load_menu(self, data):
        self.menu = Menu(self.system)

        for element_data in data["elements"]:
            element = self.create_element(element_data)
            self.menu.add_child(element)

        self.menu.on_load()
        self.current_menu = data["name"]
        self.current_view = "menu"
        return self.menu

    def load_form(self, data):
        self.form = Form(self.system)
        elements = {}

        for definition in data.get("elements", []):
            element = self.create_element(definition)
            elements[definition["id"]] = element

            if "field" in definition:
                self.form.add_field(definition["field"], element)
            else:
                self.form.add_child(element)

        if "error_element" in data:
            self.form.set_error_element(elements[data["error_element"]])
        self.current_form = data["name"]
        self.current_view = "form"
        return self.form

    def scale(self):
        if self.menu:
            self.menu.scale()
        if self.form:
            self.form.scale()

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
            return Button(self.system, element_id, data.get("font_size"), data.get("text", ""), tuple(data.get("position", [0, 0])), lambda: callback(action) if callback else None)

        elif element_type == "query":
            return Query(self.system, element_id, data.get("text", ""))

        elif element_type == "image":
            return Image(self.system, element_id, data.get("asset"), tuple(data.get("position", [0.5, 0.5])), data.get("scale", [1.0, 1.0]))

        elif element_type == "header":
                    return Header(self.system, element_id,data.get("text"),data.get("font_size"), tuple(data.get("position", [0.5, 0.5])))

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
        elif element_type == "select":
            return Select(
                self.system,
                element_id,
                tuple(data.get("position", [0, 0])),
                data.get("options")
            )

        log_error(f"Unknown UI element type: {element_type}")