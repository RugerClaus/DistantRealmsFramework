import sys
from core.util.colors import black
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.RuntimeLayer.BootSplash.state import BOOT_SPLASH_STATE
from core.util.debugoverlay import DebugOverlay
from core.loading.BootSplashManager import BootSplashManager

class Runtime:
    def __init__(self,system):

        self.system = system
        self.loading = BootSplashManager(system)
        self.debug_overlay = DebugOverlay(system)
    
    def handle_events(self):
        
        for event in self.system.input.input_event():
            command = self.system.input.handle_event(event)
            if event.type == self.system.input.video_resize_event():
                self.system.window.set_mode(event.w,event.h)
                self.debug_overlay.scale()
                if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                    self.loading.rescale_assets()
                self.system.input.rescale(event.w,event.h)

            if event.type == self.system.input.quit_event():
                self.system.runtime_state.set_state(RUNTIME_STATE.QUIT)
            
            
            elif self.system.runtime_state.is_state(RUNTIME_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.handle_event(event,command)

            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.debug_overlay.handle_event(event,command)

            self.system.sound.handle_music_event(event)

            
            if command == "debug":
                self.system.overlay_state_toggle()
            
            elif command == "developer":
                self.system.control_state_toggle()

            if event.type == self.system.input.keydown():
                if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                    if self.system.input.get_key_name(event.key) == "space" or self.system.input.get_key_name(event.key) == "return" or self.system.input.get_key_name(event.key) == "escape":
                        self.system.sound.stop_all_sfx()
                        self.system.initialize_application()
            if event.type == self.system.input.mouse_button_down() and event.button == 1:
                if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                    self.system.sound.stop_all_sfx()
                    self.system.initialize_application()
                    self.loading.state.set_state(BOOT_SPLASH_STATE.NONE)
                    self.system.clean_up_states([self.loading.state.state])
                elif self.system.runtime_state.is_state(RUNTIME_STATE.APPLICATION):
                    self.loading.state.set_state(BOOT_SPLASH_STATE.NONE)
                    self.system.clean_up_states([self.loading.state.state])

    def run(self):
        while not self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
            self.system.window.fill(black)
            self.handle_events()

            if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                self.loading.update()
                self.loading.draw()

            elif self.system.runtime_state.is_state(RUNTIME_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.update()
                    self.system.application.draw()
                else:
                    pass
            elif self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
                self.system.window.quit()
                sys.exit()
            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.debug_overlay.update()
                self.debug_overlay.draw()
            
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass

            if self.loading.state.is_state(BOOT_SPLASH_STATE.NONE):
                self.system.clean_up_states([self.loading.state.state])
            
            self.system.time.timer()
            self.system.window.update()