from core.state.ApplicationLayer.state import GAMESTATE
from core.state.ApplicationLayer.statemanager import GameStateManager
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.menus.pause import Pause
from core.application.application_object import Application_Object
from core.guts.UI.menumanager import MenuManager

class GameInterface:
    def __init__(self, system):
        self.state = GameStateManager()
        self.system = system
        self.pause_menu = Pause(system, self,self.toggle_pause)
        self.menus = MenuManager(system)
        self.menus.load()
        self.game_object = Application_Object(system,self.menus)
        
        
    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def send_debug_info_to_system(self):
        self.game_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.app_inspector.clear()
        
    def handle_event(self, event):

        if event.type == self.system.input.keydown():
            if self.system.input.get_key_name(event.key) == "escape":
                
                if self.state.is_state(GAMESTATE.PAUSED):
                    self.pause_menu.back_to_root()
                    self.toggle_pause()
                else:
                    self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)
        
        if event.type == self.system.input.video_resize_event():
            self.pause_menu.create_buttons()
            self.game_object.resize()

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.draw()

    def save_game(self):
        self.system.save_telemetry = ""
        data = {}
        self.system.save.write_save(data)
        print("saved game!")

    def load_game(self):
        load_data_dict = self.system.load.load_save()
        if load_data_dict is not None:
            pass
        else:
            self.system.save_telemetry = "No Save File Found!" # message printed to main menu
            return None
        
    def init(self):
        self.system.runtime_state.set_state(RUNTIME_STATE.APPLICATION)
        self.state.set_state(GAMESTATE.PLAYING)
        

    def save_game(self):
        self.system.save_telemetry = ""
        data = {}
        self.system.save.write_save(data)
        print("saved game!")

    def load_game(self):
        load_data_dict = self.system.load.load_save()
        if load_data_dict is not None:
            pass
        else:
            self.system.save_telemetry = "No Save File Found!" # message printed to main menu
            return None

    def reset_game(self):
        self.game_object.reset()
        self.state.set_state(GAMESTATE.PLAYING)

    def update(self):
        pass

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.system.save_telemetry = ""
        self.game_object.clean_up_states()
        self.game_object.reset()
        self.system.clean_up_states([self.state.state,self.pause_menu.state.state])
        

    def quit(self):
        self.system.quit()