
class ActionRegistrar:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        self.system = app_interface.system
    def register(self):
        application = self.app_interface
        application.actions.register("open_changelog",lambda: application.ui_controller.show_ui("changelog"))
        application.actions.register("open_credits",lambda: application.ui_controller.show_ui("credits"))
        application.actions.register("main_menu", lambda: application.ui_controller.show_ui("main"))
        application.actions.register("quit",self.system.quit)