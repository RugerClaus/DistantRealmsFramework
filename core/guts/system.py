import math
# core systems
from core.guts.input.inputmanager import InputManager
from core.guts.audioengine import AudioEngine
from core.guts.window import Window
from core.guts.save.save import Save
from core.guts.save.load import Load

# state systems
from core.state.ApplicationLayer.statemanager import StateManager
from core.state.ApplicationLayer.Debug.statemanager import DebugStateManager
from core.state.ApplicationLayer.devmanager import DevManager
from core.state.ApplicationLayer.Debug.StateMonitor.statemanager import StateMonitorStateManager

from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.Debug.state import DEBUG_STATE
from core.state.ApplicationLayer.dev import DEVELOPER_MODE

class System():
    def __init__(self):

        self.math = math

        self.app_state = StateManager()
        self.overlay_state = DebugStateManager()
        self.control_state = DevManager()
        self.state_monitor_state = StateMonitorStateManager()

        self.window = Window()
        self.sound = AudioEngine(self.app_state)
        self.input = InputManager(self.window)
        self.save = Save()
        self.load = Load()
        
    def control_state_toggle(self):
        if not self.control_state.is_state(DEVELOPER_MODE.ON):
            self.control_state.set_state(DEVELOPER_MODE.ON)
        else:
            self.control_state.set_state(DEVELOPER_MODE.OFF)

    def overlay_state_toggle(self):
        if not self.overlay_state.is_state(DEBUG_STATE.ON):
            self.overlay_state.set_state(DEBUG_STATE.ON)
        else:
            self.overlay_state.set_state(DEBUG_STATE.OFF)

    def go_to_menu(self):
        self.app_state.set_state(APPSTATE.MAIN_MENU)
        self.sound.play_music()
        
    def quit(self):
        self.app_state.set_state(APPSTATE.QUIT)