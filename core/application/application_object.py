class Application_Object:
    def __init__(self,system): # why is init the constructor. I get it initializes the class, but I would like to be free to call init/whatever form in my programs
        self.system = system

    def update(self):
        self.system.time.get_delta()

    def draw(self):
        self.system.window.fill((0,0,0))

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