from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.state import APPSTATE
from core.menus.pause import Pause
from core.application.game_object import GameObject

class GameInterface:
    def __init__(self, system):
        self.state = GameStateManager()
        self.system = system
        self.pause_menu = Pause(system, self,self.toggle_pause)
        self.game_object = GameObject(system)
        
    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def send_debug_info_to_system(self):
        self.game_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.runtime_inspector.clear()
        
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
        self.system.save.write_game_save(data)
        print("saved game!")

    def load_game(self):
        load_data_dict = self.system.load.load_game_save()
        if load_data_dict is not None:
            pass
        else:
            self.system.save_telemetry = "No Save File Found!" # message printed to main menu
            return None
        
    def init(self):
        self.system.app_state.set_state(APPSTATE.GAME)
        self.state.set_state(GAMESTATE.PLAYING)
        

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
        self.system.clean_up_states([self.state.state])
        

    def quit(self):
        self.system.quit()