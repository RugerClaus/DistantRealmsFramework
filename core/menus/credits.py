from core.ui.centertext import CenterText
from config import config

class Credits(CenterText):
    def __init__(self,system):
        super().__init__(system)
        self.authors = config["AUTHORS"]

    def draw(self):
        title = config["TITLE"]
        soundtrack = f"Soundtrack by {self.authors[0]}"
        design = f"Designed on the Distant Realms Python \n framework by {self.authors[0]}"
        logo = f"Logo by {self.authors[1]}"
        self._draw_centered_text(f"{title}\n{soundtrack}\n{design}\n{logo}\n")

    def rescale(self):
        self.draw()