import sys
from helper import *
from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.Debug.state import DEBUG_STATE
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.Loading.state import LOAD_SCREEN_STATE
from core.util.debugoverlay import DebugOverlay
from core.game.game import Game
from core.menus.menu import Menu
from core.loading.loadingmanager import LoadingManager

class App:
    def __init__(self,system):

        self.system = system
        self.game = Game(self.system)
        self.menu = Menu(self.system,self.game)
        self.loading = LoadingManager(self.system)
        self.debug_overlay = DebugOverlay(self.system,self.game,self.loading)
    
    def handle_events(self):
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
            
            if self.system.overlay_state.is_state(DEBUG_STATE.ON):
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
                elif self.system.input.get_key_name(event.key) == "u":
                    print(read_constant_from_file('username'))
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

    def run(self):
        while not self.system.app_state.is_state(APPSTATE.QUIT):
            self.system.window.fill(get_colors('black'))
            self.handle_events()

            if self.system.app_state.is_state(APPSTATE.LOADING):
                self.loading.update()
                self.loading.draw()
            
            elif self.system.app_state.is_state(APPSTATE.MAIN_MENU):
                self.menu.update()
                self.menu.draw()
            elif self.system.app_state.is_state(APPSTATE.GAME):
                self.game.update()
                self.game.draw()
            elif self.system.app_state.is_state(APPSTATE.QUIT):
                self.system.window.quit()
                sys.exit()
            if self.system.overlay_state.is_state(DEBUG_STATE.ON):
                self.debug_overlay.update()
                self.debug_overlay.draw()
            
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass

            self.system.window.timer()
            self.system.window.update()