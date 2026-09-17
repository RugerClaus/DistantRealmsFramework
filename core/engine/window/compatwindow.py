from systemlogging import log_error
from helper import asset
from config import config


class Window:

    def __init__(self, system):
        self.system = system
        self.color = (255, 0, 0)

        self.width = None
        self.height = None

        self.fps = 60
        self.fullscreen = False

        self.set_mode()

        self.Rect = self.system.backend.pygame.Rect

    # ---------------------------------------------------------
    # Compatibility / Utility
    # ---------------------------------------------------------

    def mask(self, surface):
        if hasattr(surface, "surface"):
            surface = surface.surface

        return self.system.backend.pygame.mask.from_surface(surface)

    def make_rect(self, data):
        x, y, w, h = data
        return self.Rect(x, y, w, h)

    def make_surface(self, width, height, alpha=False):
        return self.system.backend.backcompat.make_surface(
            self.system,
            (width, height),
            alpha
        )

    def load_image(self, file_like):
        image = self.system.backend.pygame.image.load(file_like)

        return self.system.backend.backcompat.upload_surface(
            None,
            image
        )

    def transform_scale(self, original, width, height):
        if isinstance(original, self.system.backend.pygame.Surface):
            return self.system.backend.pygame.transform.scale(
                original,
                (width, height)
            )

        return original.scale(width, height)

    def transform_rotate(self, original, angle):
        return original.rotate(angle)

    def transform_smoothscale(
        self,
        original,
        newW,
        newH
    ):
        return self.system.backend.pygame.transform.smoothscale(
            original,
            (newW, newH)
        )

    # ---------------------------------------------------------
    # Window
    # ---------------------------------------------------------

    def set_mode(self):

        self.system.backend.backcompat.set_mode(
            self.system,
            title=f"{config['TITLE']} {config['VERSION']}",
            resizable=True,
            fullscreen=self.fullscreen
        )

        icon = self.system.backend.pygame.image.load(
            asset("linux_icon")
        )

        self.system.backend.backcompat.set_icon(icon)


        self.renderer = self.system.backend.backcompat.renderer

    def toggle_fullscreen(self):

        self.fullscreen = not self.fullscreen

        self.set_mode()

    # ---------------------------------------------------------
    # Dimensions
    # ---------------------------------------------------------

    def get_width(self):
        return self.system.backend.backcompat.window.size[0]

    def get_height(self):
        return self.system.backend.backcompat.window.size[1]

    def get_size(self):
        return self.system.backend.backcompat.window.size

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def default_fill(self):
        self.fill(self.color)

    def fill(self, color, alpha=None):

        if isinstance(color, str):
            color = color

        elif isinstance(color, tuple) and len(color) == 3:
            alpha = alpha if alpha is not None else 255

        elif isinstance(color, tuple) and len(color) == 4:
            alpha = color[3]
            color = color[:3]

        else:
            raise ValueError(
                "fill() only supports RGB or RGBA "
                "tuples or color strings"
            )

        self.system.backend.backcompat.clear(
            color,
            alpha
        )

    def draw_overlay(self, color, alpha):

        overlay = self.make_surface(
            self.get_width(),
            self.get_height(),
            alpha=True
        )

        overlay.fill(
            (*color, alpha)
        )

        return overlay

    def draw_line(
        self,
        surface,
        point_a,
        point_b,
        color,
        width=1
    ):

        if not isinstance(color, tuple):
            log_error(
                "color must be a tuple"
            )
            return

        self.system.backend.backcompat.line(
            surface,
            point_a,
            point_b,
            color,
            width
        )

    def draw_polygon(
        self,
        surface,
        color,
        points
    ):

        self.system.backend.backcompat.polygon(
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
                "circle surface must be a pygame Surface",
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
            self.system.backend.backcompat.circle(
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

        if not isinstance(color, tuple):
            log_error(
                "color must be a tuple",
                object
            )

        if not isinstance(
            rect,
            self.system.backend.pygame.Rect
        ):
            log_error(
                "rect must be a self.system.backend.pygame.Rect"
            )
            return

        self.system.backend.backcompat.rect(
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
        area=None,
        vshader=None,
        fshader=None,
        shadervals=None,
        light_surface=None
    ):

        if area is not None:
            x, y, w, h = area

            area = self.Rect(
                x,
                y,
                w,
                h
            )

        self.system.backend.backcompat.blit(
            surface,
            destination,
            area,
            vshader,
            fshader,
            shadervals,
            light_surface
        )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    def get_screen(self):
        return self.system.backend.backcompat.get_screen()

    def update_surface(self, surface):
        self.system.backend.backcompat.update_surface(surface)

    def update(self):
        self.system.backend.backcompat.flip()

    def mark_surface_dirty(self,surface):

        self.system.backend.backcompat.surface_cache_dirty.add(id(surface))


    # ---------------------------------------------------------
    # Miscellaneous
    # ---------------------------------------------------------

    def get_fps(self):
        return self.system.time.get_fps()

    def get_info(self):
        return {
            "window": self.get_size(),
            "backend": "draw"
        }