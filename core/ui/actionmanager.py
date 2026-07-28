from systemlogging import log_error

class UIActionManager:
    def __init__(self):
        self.actions = {}

    def register(self, name, callback):
        self.actions[name] = callback

    def execute(self, name):
        if name not in self.actions:
            log_error(f"Unknown UI action: {name}","core.guts.UI.UIActionManager")
            return None
        
        return self.actions[name]()
