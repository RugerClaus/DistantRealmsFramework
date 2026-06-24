from helper import read_constant_from_file
from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.ApplicationLayer.Loading.state import LOAD_SCREEN_STATE
class GlobalEvents:

    def __init__(self,system):
        self.system = system

    def handle_system_input(self):
        for event in self.system.input.input_event():
            if event.type == self.system.input.video_resize_event():
                self.system.window.scale(event.w,event.h)
                self.debug_overlay.scale()
                if self.system.app_state.is_state(APPSTATE.LOADING):
                    self.loading.rescale_assets()
                self.menu.scale()
                self.system.input.rescale(event.w,event.h)

            if event.type == self.system.input.quit_event():
                self.system.app_state.set_state(APPSTATE.QUIT)
            
            if self.system.app_state.is_state(APPSTATE.MAIN_MENU):
                
                self.menu.handle_event(event)
                self.system.sound.stop_sfx("splash1")
                self.system.sound.stop_sfx("splash2")

            elif self.system.app_state.is_state(APPSTATE.GAME):
                self.game.handle_event(event)
            
            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.debug_overlay.handle_event(event)

            self.system.sound.handle_music_event(event)

            command = self.system.input.handle_event(event)
            if command == "debug":
                self.system.overlay_state_toggle()
            
            elif command == "developer":
                self.system.control_state_toggle()

            if event.type == self.system.input.keydown():
                if self.system.input.get_key_name(event.key) == "f11":
                    self.system.window.toggle_fullscreen()
                if self.system.app_state.is_state(APPSTATE.LOADING):
                    if self.system.input.get_key_name(event.key) == "space" or self.system.input.get_key_name(event.key) == "return" or self.system.input.get_key_name(event.key) == "escape":
                        self.system.app_state.set_state(APPSTATE.MAIN_MENU)
            if event.type == self.system.input.mouse_button_down() and event.button == 1:
                if self.system.app_state.is_state(APPSTATE.LOADING):
                    self.system.app_state.set_state(APPSTATE.MAIN_MENU)
                    self.loading.state.set_state(LOAD_SCREEN_STATE.NONE)
                elif self.system.app_state.is_state(APPSTATE.MAIN_MENU):
                    self.loading.state.set_state(LOAD_SCREEN_STATE.NONE)
                    self.menu.scale()