class ActionRegistrar:
    def __init__(self, application):
        self.application = application
        self.system = application.system

    def register(self):
        application = self.application

        application.actions.register("open_credits",lambda: self.system.ui_controller.show("credits"))
        application.actions.register("main_menu", lambda: self.system.ui_controller.show("main"))
        application.actions.register("quit",self.system.quit)