from core.state.ApplicationLayer.state import APP_STATE
from core.state.ApplicationLayer.statemanager import AppStateManager
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
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

    def toggle_freeze(self):
        print("toggling pause")
        if self.state.is_state(APP_STATE.FROZEN):
            self.state.set_state(APP_STATE.RUNNING)
        elif self.state.is_state(APP_STATE.RUNNING):
            self.state.set_state(APP_STATE.FROZEN)

    def reload_actions(self):
        import importlib
        from core.ui import actionmanager, loader
        from core.guts.UI import uicontroller
        from core.application import action_register

        current_ui = self.ui_controller.active_name

        importlib.reload(actionmanager)
        importlib.reload(loader)
        importlib.reload(uicontroller)
        importlib.reload(action_register)

        self.actions = actionmanager.UIActionManager()
        self.ui = loader.UILoader(self.system, self.actions)
        self.ui_controller = uicontroller.UIController(self.system, self.ui)

        self.action_registrar = action_register.ActionRegistrar(self)
        self.action_registrar.register()

        if current_ui:
            self.ui_controller.show_ui(current_ui)

    def reload_application(self):
        import importlib
        from core.application import application

        importlib.reload(application)

        self.app_object = application.Application(self)
            
    def send_debug_info_to_system(self):
        self.app_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.app_inspector.clear()
        
    def handle_event(self, event,command=None):
        self.ui_controller.handle_event(event)
        
        if event.type == self.system.input.video_resize_event():
            self.app_object.resize()
            self.ui_controller.scale()

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            if command == "reload_ui":
                self.reload_actions()
                print("Reloading User Interface...")
            elif command == "reload_application":
                self.reload_application()
                print("Reloading Application...")
        if self.app_object:
            if self.state.is_state(APP_STATE.RUNNING):
                self.app_object.handle_event(event,command)

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
            self.ui_controller.show_ui("MAIN")
        self.system.runtime_state.set_state(RUNTIME_STATE.APPLICATION)
        self.reload_application()
        self.action_registrar.register()

    def reset_game(self):
        self.app_object.reset()

    def update(self):
        self.ui_controller.update()
        if self.state.is_state(APP_STATE.RUNNING):
            if self.app_object:
                self.app_object.update()

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.system.save_telemetry = ""
        self.app_object.clean_up_states()
        self.app_object.reset()
        self.system.clean_up_states([self.state.state])

    def quit(self):
        self.system.quit()