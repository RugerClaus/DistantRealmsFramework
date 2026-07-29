from core.util.colors import *

class Application:
    def __init__(self,app_interface):
        self.app_interface = app_interface

    def handle_event(self,event):
        pass

    def update(self):
        pass

    def draw(self):
        self.app_interface.system.window.fill((black))

    def resize(self):
        pass

    def clean_up_states(self):
        pass

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass
