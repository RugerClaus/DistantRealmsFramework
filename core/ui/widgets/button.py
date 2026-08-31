from systemlogging import log_error, log_warning
from core.state.RuntimeLayer.UI.Button.statemanager import ButtonStateManager
from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE
from core.state.RuntimeLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.ui.render.button import ButtonRenderer
from core.ui.element import UIElement
from core.ui.type import WIDGET

class Style:
    def __init__(self,background=None,border=None,border_width=0,
                 border_radius=0,padding=5,text_color=(255,255,255)):
        self.background = background
        self.border = border
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding
        self.text_color = text_color


class Button(UIElement):
    def __init__(self,system,id,text,position,font_size=30,action=None,active=True,styles=None):
        self.system = system
        self.id = id
        super().__init__(position)
        self.font_size = font_size
        self.text = str(text)
        self.type = WIDGET.BUTTON
        hover_background = (60,60,60)
        idle_background = (40,40,40)

        if styles == "special_button":
            idle_background = (255, 165, 0)

        self.action = action
        self.active = active

        self.state = ButtonStateManager()

        self.renderer = ButtonRenderer(system)

        if not isinstance(position, tuple):
            log_error("position must be a tuple (x,y)", "Button")
            return

        if len(position) != 2:
            log_error("position must be a tuple of length 2", "Button")
            return

        self.x_ratio, self.y_ratio = position

        self.styles = {
            BUTTON_STATE.IDLE: Style(
                background=idle_background,
                border=(255,255,255),
                border_width=2,
                border_radius=8
            ),

            BUTTON_STATE.HOVER: Style(
                background=hover_background,
                border=(200,20,20),
                border_width=3,
                border_radius=8
            ),

            BUTTON_STATE.PRESS: Style(
                background=(20,20,20),
                border=(255,255,255),
                border_width=2,
                border_radius=8
            ),

            BUTTON_STATE.DISABLE: Style(
                background=(20,20,20),
                border=(100,100,100),
                border_width=2,
                border_radius=8,
                text_color=(100,100,100)
            ),

            BUTTON_STATE.FOCUSED: Style(
                background=(40,40,40),
                border=(0,255,255),
                border_width=3,
                border_radius=8
            )
        }
        if isinstance(styles, dict):
            self.styles = self.load_styles(styles)

        self.surface = None
        self.rect = None
        self.text_surface = None
        self.text_rect = None
        self.scale()


    def load_styles(self, data):
        styles = self.styles.copy()

        for state_name, style_data in data.items():
            state = BUTTON_STATE[state_name.upper()]

            if state not in styles:
                styles[state] = Style()

            current = styles[state]

            styles[state] = Style(
                background=tuple(style_data["background"]) if "background" in style_data else current.background,
                border=tuple(style_data["border"]) if "border" in style_data else current.border,
                border_width=style_data["border_width"] if "border_width" in style_data else current.border_width,
                border_radius=style_data["border_radius"] if "border_radius" in style_data else current.border_radius,
                padding=style_data["padding"] if "padding" in style_data else current.padding,
                text_color=tuple(style_data["text_color"]) if "text_color" in style_data else current.text_color
            )

        return styles

    def scale(self, preserve_position=False):
        self.font = self.system.font.get_font(self.font_size)
        old_center = self.rect.center if preserve_position and self.rect is not None else None

        current_style = self.styles[self.state.state]

        self.text_surface = self.font.render(self.text,True,current_style.text_color)

        self.width = self.text_surface.get_width() + current_style.padding * 2 + current_style.border_width * 2

        self.height = self.text_surface.get_height() + current_style.padding * 2 + current_style.border_width * 2

        self.surface = self.system.window.make_surface(self.width,self.height,True)

        if old_center is not None:
            center = old_center
        else:
            ww = self.system.window.get_width()
            wh = self.system.window.get_height()

            center = (int(ww * self.x_ratio),int(wh * self.y_ratio))

        self.rect = self.surface.get_rect(center=center)

        self.text_rect = self.text_surface.get_rect(center=self.surface.get_rect().center)


    def update(self, mouse_pos):

        if not self.active:
            changed = self.state.set_state(BUTTON_STATE.DISABLE)

        elif self.rect.collidepoint(mouse_pos):
            changed = self.state.set_state(BUTTON_STATE.HOVER)

        else:
            changed = self.state.set_state(BUTTON_STATE.IDLE)

        if changed:
            self.scale(preserve_position=True)

        if changed and self.state.is_state(BUTTON_STATE.HOVER):
            self.system.sound.play_ui_sfx("button_hover")


    def draw(self, target=None):
        self.renderer.draw(self, target)

    def set_text(self, text):
        print(f"Changing '{self.text}' -> '{text}'")
        self.text = str(text)
        self.scale()


    def is_clicked(self, mouse_pos, mouse_click):
        if self.active and self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                if self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                    self.system.sound.play_ui_sfx('button_clicked')
                else:
                    log_warning(f'interface sfx is disabled.{self.system.sound.interface_sfx_state.get_state()}')
                self.state.set_state(BUTTON_STATE.PRESS)
                self.clean_up_states()
                self.action()
                return True
            if not self.action:
                self.action = None

    def clean_up_states(self):
        self.system.clean_up_states([self.state.state])