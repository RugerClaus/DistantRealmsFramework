from systemlogging import log_error
from helper import asset
from config import config


class Window:

    def __init__(self, system):
        self.system = system

        self.default_width = 1600
        self.default_height = 900
        self.color = (255, 0, 0)

        self.width = None
        self.height = None

        self.fps = 60
        self.fullscreen = False

        self.set_mode(self.width, self.height)

        self.Rect = self.system.backend.pygame.Rect

    # ---------------------------------------------------------
    # Compatibility / Utility
    # ---------------------------------------------------------

    def mask(self, surface):
        return self.system.backend.pygame.mask.from_surface(surface)

    def make_rect(self, data):
        x, y, w, h = data
        return self.Rect(x, y, w, h)

    def make_surface(self, width, height, alpha=False):
        flags = self.system.backend.pygame.SRCALPHA if alpha else 0
        return self.system.backend.pygame.Surface(
            (width, height),
            flags
        )

    def load_image(self, file_like):
        image = self.system.backend.pygame.image.load(file_like)
        image = image.convert_alpha()
        return image.copy()

    def transform_scale(
        self,
        original_surface,
        new_surface_width,
        new_surface_height
    ):
        return self.system.backend.pygame.transform.scale(
            original_surface,
            (
                new_surface_width,
                new_surface_height
            )
        )

    def transform_smoothscale(self, original, newW, newH):
        return self.system.backend.pygame.transform.smoothscale(
            original,
            (newW, newH)
        )

    # ---------------------------------------------------------
    # Window
    # ---------------------------------------------------------

    def set_mode(self, width=None, height=None, mode=None):

        width = (
            width
            if width is not None
            else self.default_width
        )

        height = (
            height
            if height is not None
            else self.default_height
        )

        self.width = width
        self.height = height

        self.system.backend.draw.init(
            width,
            height,
            title=f"{config['TITLE']} {config['VERSION']}",
            fullscreen=self.fullscreen
        )

        icon = self.load_image(asset("linux_icon"))
        self.system.backend.draw.set_icon(icon)

    def toggle_fullscreen(self):

        self.fullscreen = not self.fullscreen

        self.set_mode()

    # ---------------------------------------------------------
    # Dimensions
    # ---------------------------------------------------------

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return (
            self.width,
            self.height
        )

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def default_fill(self):
        self.fill(self.color)

    def fill(self, color, alpha=None):

        if isinstance(color, str):
            color = color

        elif isinstance(color, tuple) and len(color) == 3:
            alpha = (
                alpha
                if alpha is not None
                else 255
            )

            color = (*color, alpha)

        elif isinstance(color, tuple) and len(color) == 4:
            color = color

        else:
            raise ValueError(
                "fill() only supports RGB or RGBA "
                "tuples or color strings"
            )

        self.system.backend.draw.draw.clear(color)

    def draw_overlay(self, color, alpha):

        overlay = self.make_surface(
            self.get_width(),
            self.get_height(),
            alpha=True
        )

        overlay.fill((*color, alpha))

        return overlay

    def draw_line(
        self,
        surface,
        point_a,
        point_b,
        color,
        width=None
    ):

        if isinstance(color, tuple):

            self.system.backend.draw.draw.line(
                surface,
                point_a,
                point_b,
                color,
                width
            )

        else:
            log_error("color must be a tuple")

    def draw_polygon(
        self,
        surface,
        color,
        points
    ):

        self.system.backend.draw.draw.polygon(
            surface,
            color,
            points
        )

    def draw_circle(
        self,
        surface,
        color,
        center,
        radius,
        object=None
    ):

        if not isinstance(
            surface,
            self.system.backend.pygame.Surface
        ):
            log_error(
                "circle surface must be a Surface",
                object
            )

        elif (
            not isinstance(color, tuple)
            or len(color) != 3
        ):
            log_error(
                f"color must be a tuple: (r,g,b); "
                f"found: value: {str(color)} "
                f"type: {str(type(color))}",
                object
            )

        elif (
            not isinstance(center, tuple)
            or len(center) != 2
        ):
            log_error(
                f"center must be a tuple: (x,y); "
                f"found: value: {str(center)} "
                f"type: {str(type(center))}",
                object
            )

        elif not isinstance(radius, float):
            log_error(
                f"radius must be a floating point number "
                f"(decimal); found: value: {str(radius)} "
                f"type: {str(type(radius))}",
                object
            )

        else:
            self.system.backend.draw.draw.circle(
                surface,
                color,
                center,
                radius,
                object
            )

    def draw_rect(
        self,
        surface,
        color,
        rect,
        width=0,
        border_radius=None,
        object=None
    ):

        if not isinstance(
            surface,
            self.system.backend.pygame.Surface
        ):
            log_error(
                "rect surface must be a Surface",
                object
            )
            return

        elif not isinstance(color, tuple):
            log_error(
                "color must be a tuple",
                object
            )

        elif not isinstance(
            rect,
            self.system.backend.pygame.Rect
        ):
            log_error(
                "rect must be a self.system.backend.pygame.Rect"
            )

        self.system.backend.draw.draw.rect(
            surface,
            color,
            rect,
            width,
            border_radius,
            object
        )

    def blit(
        self,
        surface,
        destination,
        area=None
    ):

        if area is not None:
            x, y, w, h = area

            area = self.Rect(
                x,
                y,
                w,
                h
            )

        self.system.backend.draw.draw.blit(
            surface,
            destination,
            area
        )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    def get_screen(self):
        return self.system.backend.draw.get_screen()

    def update(self):
        self.system.backend.draw.present()

    # ---------------------------------------------------------
    # Miscellaneous
    # ---------------------------------------------------------

    def get_fps(self):
        return self.system.time.get_fps()

    def get_info(self):
        return self.system.backend.draw.get_info()

    def quit(self):
        return self.system.backend.draw.quit()