import math,random,os,json,sys
from config import config
# core systems
from core.engine.backends.backend import Backend
from core.engine.input.inputmanager import InputManager
from core.engine.audioengine import AudioEngine
from core.engine.time import Time
from core.engine.persistence.persistence import Persistence
from core.engine.network.update import Update
from core.engine.network.network import Network
from core.engine.user import User
from core.engine.telemetry import system_monitor
from core.loading.BootSplashManager import BootSplashManager

from core.ui.font import FontEngine

from application.save_schema import schema

# state systems
from core.state.RuntimeLayer.NetworkLayer.Login.statemanager import LoginStateManager
from core.state.RuntimeLayer.statemanager import RuntimeStateManager
from core.state.RuntimeLayer.DevTools.Debug.statemanager import DebugStateManager
from core.state.RuntimeLayer.DevTools.DeveloperMode.statemanager import DeveloperModeStateManager
from core.state.RuntimeLayer.DevTools.StateMonitor.statemanager import StateMonitorStateManager

from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.DevTools.Debug.state import DEBUG_OVERLAY_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.RuntimeLayer.DevTools.StateMonitor.state import MONITOR_STATE
class System():
    def __init__(self):

        self.math = math
        self.random = random
        self.os = os
        self.json = json
        self.sys = sys

        self.runtime_state = RuntimeStateManager()
        self.overlay_state = DebugStateManager()
        self.control_state = DeveloperModeStateManager()
        self.state_monitor_state = StateMonitorStateManager()
        self.login_state = LoginStateManager()

        self.backend = Backend(self)

        self.time = Time(self)

        self.save_schema = schema
        self.system_monitor = system_monitor # this is an observer

        self.persistence = Persistence(self)
        self.persistence.save.save_schema = self.save_schema

        self.updater = Update()
        self.network = Network()

        self.user = User(self)

        print("pygame initialized:", self.backend.pygame.get_init())
        print("display initialized:", self.backend.pygame.display.get_init())

        self.load_window()
        self.font = FontEngine(self)
        self.sound = AudioEngine(self)
        self.input = InputManager(self)

        self.app_inspector = {} # this is an observer
        self.save_telemetry = "" # this sends a message to the main menu if there is no save file found

        self.system_monitor["Distant Realms Version"] = config.get("FRAMEWORK VERSION")

        if self.network.check_network_status():
            self.system_monitor["network"] = "Connected"
        else:
            self.system_monitor["network"] = "Not Connected"
    
        self.system_monitor["OS"] = config.get("OS") 
        
        self.loading = None
        self.application = None

        if self.control_state.is_state(DEVELOPER_MODE.ON):
            self.sound.volume = 0.0
            self.sound.sfx_volume = 0.1

        if config.get("SPLASHSCREEN") == True:
            self.loading = BootSplashManager(self)
        else:
            self.initialize_application()

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
        
    def quit(self):
        if self.application:
            self.application.clean_up()
        self.runtime_state.set_state(RUNTIME_STATE.QUIT)
        if config["WINDOW_BACKEND"] == "pygame":
            self.backend.pygame.quit()
            self.sys.exit()
        elif config["WINDOW_BACKEND"] == "draw":
            self.backend.draw.quit()
            self.sys.exit()

    def initialize_application(self):
        from core.engine.distant_realms import DistantRealms
        self.runtime_state.set_state(RUNTIME_STATE.APPLICATION)
        self.state_monitor_state.set_state(MONITOR_STATE.APPLICATION)
        self.application = DistantRealms(self)
        self.application.init()

    def clean_up_states(self, states):
        collections = (
            self.runtime_state.active_application_states,
            self.runtime_state.active_system_states,
            self.runtime_state.active_runtime_states,
            self.runtime_state.all_active_states,
        )

        for state in states:
            for collection in collections:
                if state in collection:
                    collection.remove(state)

    def load_window(self):
        import importlib
        import sys

        backend = config.get("WINDOW_BACKEND", "pygame").lower()

        if backend == "pygame":
            module_name = "core.engine.window.pgwindow"
        elif backend == "draw":
            module_name = "core.engine.window.drwindow"
        else:
            raise ValueError(f"Unknown window backend: {backend}")

        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        self.window = module.Window(self)