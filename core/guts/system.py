import math,random,os
from systemlogging import log_event
# core systems
from core.guts.input.inputmanager import InputManager
from core.guts.audioengine import AudioEngine
from core.guts.window import Window
from core.guts.time import Time
from core.guts.save.save import Save
from core.guts.save.load import Load
from core.guts.network import Network
from core.application.runtime_inspector import runtime_inspector
from core.application.save_schema import schema
from core.guts.telemetry import system_monitor

# state systems
from core.state.ApplicationLayer.statemanager import StateManager
from core.state.ApplicationLayer.DevTools.Debug.statemanager import DebugStateManager
from core.state.ApplicationLayer.devmanager import DevManager
from core.state.ApplicationLayer.DevTools.Debug.StateMonitor.statemanager import StateMonitorStateManager

from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.DevTools.Debug.StateMonitor.state import MONITOR_STATE

class System():
    def __init__(self):

        self.math = math
        self.random = random

        self.app_state = StateManager()
        self.overlay_state = DebugStateManager()
        self.control_state = DevManager()
        self.state_monitor_state = StateMonitorStateManager()

        self.network = Network()

        self.time = Time()

        self.save_schema = schema
        
        self.save = Save(self.save_schema)
        self.load = Load()

        self.window = Window(self)
        self.sound = AudioEngine(self)
        self.input = InputManager(self)

        self.system_monitor = system_monitor

        self.runtime_inspector = runtime_inspector # this is an observer
        self.save_telemetry = "" # this sends a message to the main menu if there is no save file found

        if self.network.check_network_status():
            self.system_monitor["network"] = "Connected"
        else:
            self.system_monitor["network"] = "Not Connected"

        self.application = None

    def control_state_toggle(self):
        if not self.control_state.is_state(DEVELOPER_MODE.ON):
            self.control_state.set_state(DEVELOPER_MODE.ON)
        else:
            self.control_state.set_state(DEVELOPER_MODE.OFF)

    def overlay_state_toggle(self):
        if not self.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
            self.overlay_state.set_state(DEBUG_OVERLAY_STATE.ON)
        else:
            self.overlay_state.set_state(DEBUG_OVERLAY_STATE.OFF)

    def go_to_menu(self):
        self.app_state.set_state(APPSTATE.MAIN_MENU)
        if self.application is not None:
            self.application.quit_to_menu()
            self.application = None
        self.sound.play_music()

    def reset_application(self):
        if self.application:
            self.application.reset_game()
        
    def quit(self):
        self.app_state.set_state(APPSTATE.QUIT)

    def create_volume_files(self,default_volume):
        file_path = 'saves/constants'
        if not os.path.exists(f'{file_path}'):
            os.makedirs(f'{file_path}')
        
        if not os.path.exists(f"{file_path}/music_volume"):
            self.save.write_constant('music_volume',f'{default_volume}')
            log_event('Music volume file creation: music_volume file created')
        else:
            log_event('Music volume file creation: music_volume file exists')
        
        if not os.path.exists(f"{file_path}/sfx_volume"):
            self.save.write_constant('sfx_volume',f'{default_volume}')
            log_event('SFX volume file creation: sfx_volume file created')
        else:
            log_event('SFX volume file creation: sfx_volume file exists')

    def initialize_application(self):
        from core.application.game import GameInterface
        self.app_state.set_state(APPSTATE.GAME)
        self.state_monitor_state.set_state(MONITOR_STATE.GAME)
        self.application = GameInterface(self)
        self.application.init()
        

    def clean_up_states(self, states):
        collections = (
            self.app_state.active_application_states,
            self.app_state.active_system_states,
            self.app_state.active_game_states,
            self.app_state.all_active_states,
        )

        for state in states:
            for collection in collections:
                if state in collection:
                    collection.remove(state)