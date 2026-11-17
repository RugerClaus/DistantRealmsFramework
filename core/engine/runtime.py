from config import config

from core.util.colors import black
from core.state.SystemLayer.state import SYSTEM_STATE
from core.state.SystemLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.SystemLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.SystemLayer.DevTools.Console.state import CONSOLE_STATE

class Runtime:
    def __init__(self,system):
        self.system = system

        self.system.input.CommandModule.sequences["quick_quit"] = [self.system.input.keys.F12_key()]
    
    def handle_events(self):
        for event in self.system.input.input_event():
            command = self.system.input.handle_event(event)
            if event.type == self.system.input.video_resize_event():
                self.system.font.scale(event.w,event.h)
                self.system.debug_overlay.scale()
                self.system.command_console.scale()
                if self.system.loading:
                    self.system.loading.scale()
                self.system.input.scale(event.w,event.h)

            

            if event.type == self.system.input.quit_event():
                self.system.system_state.set_state(SYSTEM_STATE.QUIT)
            
            elif self.system.system_state.is_state(SYSTEM_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.handle_event(event,command)

            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.system.debug_overlay.handle_event(event,command)

            if self.system.console_state.is_state(CONSOLE_STATE.ON):
                self.system.command_console.handle_event(event,command)
                continue

            self.system.sound.handle_music_event(event)

            if command == "debug":
                self.system.overlay_state_toggle()
            
            elif command == "developer":
                self.system.control_state_toggle()

            elif command == "console":
                self.system.console_state_toggle()

            elif command == "quick_quit":
                self.system.quit()

            if self.system.loading:
                self.system.loading.handle_event(event,command)
    def run(self):
        while not self.system.system_state.is_state(SYSTEM_STATE.QUIT):
            self.system.window.fill(black)
            self.system.backend.backcompat.process_gpu_tasks()
            self.handle_events()

            if self.system.system_state.is_state(SYSTEM_STATE.SPLASH):
                self.system.loading.update()
                self.system.loading.draw()

            elif self.system.system_state.is_state(SYSTEM_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.update()
                    self.system.application.draw()
            elif self.system.system_state.is_state(SYSTEM_STATE.QUIT):
                self.system.quit()
            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.system.debug_overlay.update()
                self.system.debug_overlay.draw()
            
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass

            if self.system.console_state.is_state(CONSOLE_STATE.ON) or self.system.command_console.console_output.fading:
                self.system.command_console.update()
                self.system.command_console.draw()
                
            self.system.time.timer()
            self.system.window.update()