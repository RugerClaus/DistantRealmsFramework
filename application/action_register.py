
class ActionRegistrar:
    def __init__(self, distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system
        
    def register(self):
        application = self.distant_realms
        application.actions.register("open_changelog",lambda: application.ui_controller.show_ui("changelog"))
        application.actions.register("open_credits",lambda: application.ui_controller.show_ui("credits"))
        application.actions.register("main_menu", lambda: application.ui_controller.show_ui("main"))
        application.actions.register("test_button", lambda: print("Testing"))
        application.actions.register("quit",self.system.quit)