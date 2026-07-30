from pathlib import Path

from systemlogging import log_event

from core.guts.persistence.save import Save
from core.guts.persistence.load import Load

class Persistence:
    def __init__(self, system, project_root=None):
        self.system = system

        self.engine_root = Path("enginepersistence")

        self.project_root = Path(project_root) if project_root else None

        self.engine_menus = self.engine_root / "menus"
        self.engine_forms = self.engine_root / "forms"

        self.project_menus = self.project_root / "menus" if self.project_root else None
        self.project_forms = self.project_root / "forms" if self.project_root else None

        self.save = Save()
        self.load = Load()

    def get_menu(self, name):
        filename = f"{name.upper()}.json"

        if self.project_menus:
            path = self.project_menus / filename
            log_event("Checking project menu:", path.resolve())
            if path.exists():
                log_event("Found project menu")
                return path

        path = self.engine_menus / filename
        log_event("Checking engine menu:", path.resolve())
        log_event("Exists:", path.exists())
        return path

    def get_form(self, name):
        filename = f"{name.upper()}.json"

        if self.project_forms:
            path = self.project_forms / filename
            if path.exists():
                return path

        return self.engine_forms / filename