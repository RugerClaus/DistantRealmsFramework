import sys
from core.util.colors import black
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.util.debugoverlay import DebugOverlay

class Runtime:
    def __init__(self,system):

        self.system = system
        self.debug_overlay = DebugOverlay(system)
    
    def handle_events(self):
        for event in self.system.input.input_event():
            command = self.system.input.handle_event(event)
            if event.type == self.system.input.video_resize_event():
                self.system.font.scale(event.w,event.h)
                self.debug_overlay.scale()
                if self.system.loading:
                    self.system.loading.scale()
                self.system.input.scale(event.w,event.h)

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

            if self.system.loading:
                self.system.loading.handle_event(event,command)
    def run(self):
        while not self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
            self.system.window.fill(black)
            self.handle_events()

            if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                self.system.loading.update()
                self.system.loading.draw()

            elif self.system.runtime_state.is_state(RUNTIME_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.update()
                    self.system.application.draw()
            elif self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
                self.system.window.quit()
                sys.exit()
            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.debug_overlay.update()
                self.debug_overlay.draw()
            
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass
            
            self.system.time.timer()
            self.system.window.update()