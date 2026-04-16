from helper import log_event, log_error
from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.state import APPSTATE
from core.menus.pause import Pause

class Game:
    def __init__(self, system):
        self.state = GameStateManager()
        self.system = system
        self.pause_menu = Pause(system, self,self.quit_to_menu)
        
    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def send_debug_info_to_system(self):
        # exmaple:
        # self.system.runtime_inspector["seed"] = self.world.seed
        pass
    
    def remove_debug_info_from_system(self):
        # example: 
        # self.system.runtime_inspector["seed"] = None
        pass
        
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

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            pass

    def save_game(self):
        self.system.save_telemetry = ""
        data = {}
        self.system.save.write_game_save(data)
        print("saved game!")

    def load_game(self):
        load_data_dict = self.system.load.load_game_save()
        if load_data_dict is not None:
            pass
        else:
            self.system.save_telemetry = "No Save File Found!" # message printed to main menu
            return None

    def update(self):
        pass

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.system.save_telemetry = ""
        self.system.go_to_menu()

    def quit(self):
        self.system.app_state.set_state(APPSTATE.QUIT)