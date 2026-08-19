from core.util.colors import *
from core.state.RuntimeLayer.Audio.Music.state import MUSIC_STATE

class Application:
    def __init__(self,distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system

        # UNCOMMENT BELOW IF YOU WANT TO PLAY YOUR MUSIC FILES ON STARTUP

        # if self.system.sound.music_state.is_state(MUSIC_STATE.ON):
        #     self.system.sound.play_music()

    def handle_event(self,event,command=None):
        pass

    def update(self):
        pass

    def draw(self):
        self.distant_realms.system.window.fill((black))

    def scale(self):
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

    