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

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        ui_type = data["type"]

        if ui_type == "menu":
            ui = Menu(self.system)
            self._build_menu(ui, data)

        elif ui_type == "form":
            ui = Form(self.system)
            self._build_form(ui, data)

        else:
            raise ValueError(f"Unknown UI type: {ui_type}")

        ui.on_load()
        return ui, data["name"], data["type"]

    def _build_menu(self, menu, data):
        for definition in data.get("elements", []):
            menu.add_child(self.create_element(definition))

    def _build_form(self, form, data):
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

    def create_element(self, data):
        element_type = data["type"]
        element_id = data.get("id")

        if element_type == "label":
            return Label(
                self.system,
                element_id,
                data.get("text", ""),
                tuple(data.get("position", [0, 0])),
                font_size=data.get("font_size", 30),
                color=tuple(data.get("color", [255, 255, 255]))
            )

        elif element_type == "textbox":
            element = TextBox(
                self.system,
                element_id,
                tuple(data.get("position", [0, 0])),
                tuple(data.get("dimensions", [0.1432, 0.0926])),
                font_size=data.get("font_size", 30),
                is_active=data.get("active", False)
            )

            element.is_password = data.get("password", False)
            return element

        elif element_type == "button":
            action = data.get("action")
            callback = self.actions.execute if action else None

            return Button(
                self.system,
                element_id,
                data.get("font_size"),
                data.get("text", ""),
                tuple(data.get("position", [0, 0])),
                lambda: callback(action) if callback else None,
                styles=data.get("styles")
            )

        elif element_type == "query":
            return Query(
                self.system,
                element_id,
                data.get("text", "")
            )

        elif element_type == "image":
            return Image(
                self.system,
                element_id,
                data.get("asset"),
                tuple(data.get("position", [0.5, 0.5])),
                data.get("scale", [1.0, 1.0])
            )

        elif element_type == "header":
            return Header(
                self.system,
                element_id,
                data.get("text"),
                data.get("font_size"),
                tuple(data.get("position", [0.5, 0.5])),
                color=tuple(data.get("color", [255, 255, 255]))
            )

        elif element_type == "scrollable_text":
            element = ScrollableText(
                self.system,
                element_id,
                font_size=data.get("font_size", 40),
                anchor=tuple(data.get("position", [0.5, 0.5])),
                width=data.get("width", 0.8),
                height=data.get("height", 0.6),
                align=data.get("align", "left"),
                line_spacing=data.get("line_spacing", 0.01),
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