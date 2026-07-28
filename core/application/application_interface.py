from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.application.application_object import Application_Object
from core.ui.loader import UILoader
from core.ui.actionmanager import UIActionManager
from core.application.action_register import ActionRegistrar

class AppInterface:
    def __init__(self, system):
        self.system = system
        
        self.actions = UIActionManager()
        self.game_object = Application_Object(system)
        self.ui = UILoader(system,self.actions)
        self.action_registrar = ActionRegistrar(self)
        
        self.action_registrar.register()
        

    def send_debug_info_to_system(self):
        self.game_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.app_inspector.clear()
        
    def handle_event(self, event):
        self.system.ui_controller.handle_event(event)

        if event.type == self.system.input.video_resize_event():
            self.game_object.resize()
            self.active_ui.scale()

    def draw(self):
        self.system.ui_controller.draw()

    def save_game(self):
        self.system.save_telemetry = ""
        data = {}
        self.system.persistence.save.write_save(data)
        print("saved game!")

    def load_game(self):
        load_data_dict = self.system.persistence.load.load_save()
        if load_data_dict is not None:
            pass
        else:
            self.system.save_telemetry = "No Save File Found!" # message printed to main menu
            return None
        
    def init(self):
        main_menu = self.system.persistence.get_menu("MAIN")

        if main_menu.exists():
            self.system.ui_controller.show("MAIN")
            self.system.sound.play_music("LoFiSi")

        self.system.runtime_state.set_state(RUNTIME_STATE.APPLICATION)

    def reset_game(self):
        self.game_object.reset()

    def update(self):
        self.system.ui_controller.update()

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.system.save_telemetry = ""
        self.game_object.clean_up_states()
        self.game_object.reset()
        self.system.clean_up_states([self.state.state,self.pause_menu.state.state])
        

    def quit(self):
        self.system.quit()