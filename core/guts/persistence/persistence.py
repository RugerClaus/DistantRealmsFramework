from pathlib import Path
from config import config

from systemlogging import log_event,log_warning

from core.guts.persistence.save import Save
from core.guts.persistence.load import Load
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE


class Persistence:
    def __init__(self, system):
        self.system = system
        
        self.install_root = Path(__file__).resolve().parents[4]/ "enginepersistence"
        log_warning(self.install_root)

        self.workspace_root = Path(__file__).resolve().parents[3] / "enginepersistence"
        log_warning(self.workspace_root)

        self.install_engine_root = self.install_root

        self.workspace_engine_root = self.workspace_root

        self.install_menus = self.install_engine_root / "menus"
        self.install_forms = self.install_engine_root / "forms"

        self.workspace_menus = self.workspace_engine_root / "menus"
        self.workspace_forms = self.workspace_engine_root / "forms"


        self.save = Save()
        self.load = Load()

    def developer_mode(self):
        return self.system.control_state.is_state(DEVELOPER_MODE.ON)

    def can_edit_engine_ui(self):
        return self.developer_mode()

    def get_menu(self, name):
        filename = f"{name.upper()}.json"

        path = self.workspace_menus / filename
        if path.exists():
            log_event(f"Found workspace menu: {path}", "Persistence.get_menu")
            return path

        path = self.install_menus / filename
        if path.exists():
            log_event(f"Found installed menu: {path}", "Persistence.get_menu")
            return path
        
        return path

    def get_form(self, name):
        filename = f"{name.upper()}.json"

        path = self.workspace_forms / filename
        if path.exists():
            log_event(f"Found workspace form: {path}", "Persistence.get_form")
            return path

        path = self.install_forms / filename
        if path.exists():
            log_event(f"Found installed form: {path}", "Persistence.get_form")
            return path

        return path

    
    def save_engine_ui(self, path, data):
        if not self.can_edit_engine_ui():
            log_event("Blocked engine UI write: developer mode disabled", "Persistence.save_engine_ui")
            return False

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

        log_event("Saved engine UI:", path)
        return True