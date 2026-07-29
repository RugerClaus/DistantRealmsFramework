from core.state.ApplicationLayer.state import APP_STATE
from core.state.ApplicationLayer.statemanager import AppStateManager
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.application.application_object import Application_Object
from core.ui.loader import UILoader
from core.ui.actionmanager import UIActionManager
from core.application.action_register import ActionRegistrar
from core.guts.UI.uicontroller import UIController

class AppInterface:
    def __init__(self, system):
        self.system = system

        self.state = AppStateManager()
        self.actions = UIActionManager()
        self.ui = UILoader(system, self.actions)
        self.ui_controller = UIController(system, self.ui)

        self.app_object = None
        self.action_registrar = ActionRegistrar(self)

    def reload_actions(self):
        import importlib
        from core.application import action_register

        importlib.reload(action_register)

        self.action_registrar = action_register.ActionRegistrar(self)
        self.action_registrar.register()

    def reload_application(self):
        import importlib
        from core.application import application_object

        importlib.reload(application_object)

        self.app_object = application_object.Application_Object(self)
            
    def send_debug_info_to_system(self):
        self.app_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.app_inspector.clear()
        
    def handle_event(self, event):
        self.ui_controller.handle_event(event)

        if event.type == self.system.input.video_resize_event():
            self.app_object.resize()
            self.ui.scale()

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            if event.type == self.system.input.keydown():
                if event.key == self.system.input.keys.F1_key():
                    if self.ui.current_view == "form":
                        self.ui_controller.show_form(self.ui.current_form)
                    elif self.ui.current_view == "menu":
                        self.ui_controller.show_menu(self.ui.current_menu)
                    self.reload_actions()

                if event.key == self.system.input.keys.F2_key():
                    self.reload_application()
                    print("reloading app")

    def draw(self):
        if self.app_object:
            self.app_object.draw()
        self.ui_controller.draw()

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
            self.ui_controller.show_menu("MAIN")
            self.system.sound.play_music("LoFiSi")

        self.system.runtime_state.set_state(RUNTIME_STATE.APPLICATION)

        self.app_object = Application_Object(self)

        # Now app_object exists.
        self.action_registrar.register()

    def reset_game(self):
        self.app_object.reset()

    def update(self):
        self.ui_controller.update()

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.system.save_telemetry = ""
        self.app_object.clean_up_states()
        self.app_object.reset()
        self.system.clean_up_states([self.state.state,self.pause_menu.state.state])

    def quit(self):
        self.system.quit()