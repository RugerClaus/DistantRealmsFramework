from pathlib import Path

from core.guts.persistence.save import Save
from core.guts.persistence.load import Load


class Persistence:
    def __init__(self, system):
        self.system = system

        self.root = Path("core/application/enginepersistence")

        self.menus = self.root / "menus"
        self.forms = self.root / "forms"

        self.save = Save()
        self.load = Load()

    def get_menu(self, name):
        return self.menus / f"{name.upper()}.json"

    def get_form(self, name):
        return self.forms / f"{name.upper()}.json"