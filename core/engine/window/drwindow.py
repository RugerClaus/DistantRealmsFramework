from config import config
from core.draw.renderer import Renderer
from core.draw.geometry.geometry import Geometry


class Window:

    def __init__(self,system):

        self.system = system

        self.window = system.backend.pygame.Window(
            title=f"{config['TITLE']} {config['VERSION']}",
            size=(1600,900),
            resizable=True,
            fullscreen=False,
            opengl=True
        )

        self.renderer = Renderer(self.window)

        Geometry.init(self.renderer)

        self.renderer.update_viewport()