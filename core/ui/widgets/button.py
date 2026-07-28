from systemlogging import log_error, log_warning
from core.state.RuntimeLayer.UI.Button.statemanager import ButtonStateManager
from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE
from core.state.RuntimeLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.ui.font import FontEngine
from core.ui.render.button import ButtonRenderer
from core.ui.element import UIElement
from core.ui.type import WIDGET

class Style:
    def __init__(
        self,
        background=None,
        border=None,
        border_width=0,
        border_radius=0,
        padding=5,
        text_color=(255,255,255)
    ):
        self.background = background
        self.border = border
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding
        self.text_color = text_color


class Button(UIElement):
    def __init__(self,system,id,font,text,position,action=None,active=True,styles=None):
        self.system = system
        self.id = id
        super().__init__(position)
        if font < 50:
            font = 50
        self.font = FontEngine(font).font
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

        if isinstance(styles, dict):
            self.styles = styles
        else:
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

        self.surface = None
        self.rect = None
        self.text_surface = None
        self.text_rect = None

        self.scale()


    def scale(self):

        current_style = self.styles[self.state.state]

        self.text_surface = self.font.render(
            self.text,
            True,
            current_style.text_color
        )

        self.width = (
            self.text_surface.get_width()
            + current_style.padding * 2
        )

        self.height = (
            self.text_surface.get_height()
            + current_style.padding * 2
        )


        self.surface = self.system.window.make_surface(
            self.width,
            self.height,
            True
        )


        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        x = int(ww * self.x_ratio)
        y = int(wh * self.y_ratio)


        self.rect = self.surface.get_rect(
            center=(x,y)
        )

        self.text_rect = self.text_surface.get_rect(
            center=self.surface.get_rect().center
        )


    def update(self, mouse_pos):

        if not self.active:
            changed = self.state.set_state(BUTTON_STATE.DISABLE)

        elif self.rect.collidepoint(mouse_pos):
            changed = self.state.set_state(BUTTON_STATE.HOVER)

        else:
            changed = self.state.set_state(BUTTON_STATE.IDLE)


        if changed and self.state.is_state(BUTTON_STATE.HOVER):
            self.system.sound.play_ui_sfx("button_hover")

    def draw(self):
        self.renderer.draw(self)


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