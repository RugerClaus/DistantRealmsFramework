from core.util.colors import *

class Application:
    def __init__(self,app_interface):
        self.app_interface = app_interface
        self.system = app_interface.system

    def handle_event(self,event,command=None):
        pass

    def update(self):
        pass

    def draw(self):
        self.app_interface.system.window.fill((black))

    def resize(self):
        pass

    def clean_up_states(self):
        self.system.app_inspector.clear()
        self.system.clean_up_states([]) # pass XStateManager.state in the list

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass

    