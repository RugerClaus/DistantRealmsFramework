from config import config
from helper import asset


class Window:

    def __init__(self, system):
        self.system = system

        self.default_width = 1600
        self.default_height = 900

        self.width = None
        self.height = None

        self.fps = 60
        self.fullscreen = False

        self.set_mode()

    # ---------------------------------------------------------
    # Window setup
    # ---------------------------------------------------------

    def set_mode(self, width=None, height=None, mode=None):
        width = width or self.default_width
        height = height or self.default_height

        pygame = self.system.backend.pygame

        self.window = pygame.Window(
            title=f"{config['TITLE']} {config['VERSION']}",
            size=(width, height),
            resizable=True,
            opengl=True,
            fullscreen_desktop=self.fullscreen
        )

        self.width = width
        self.height = height

        self._setup_2d()

        icon = self.load_image(asset("linux_icon"))
        self.window.set_icon(icon)

    def _setup_2d(self):
        """
        Configure OpenGL so that coordinates work like Pygame.

        (0, 0) is the top-left corner.
        X increases to the right.
        Y increases downward.
        """

        gl = self.system.backend.opengl

        # Match OpenGL's viewport to the window size.
        gl.glViewport(
            0,
            0,
            self.width,
            self.height
        )

        # Use pixel coordinates instead of OpenGL's default
        # normalized coordinate system.
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glOrtho(
            0,
            self.width,
            self.height,
            0,
            -1,
            1
        )

        # Reset the model transformation.
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Allow transparent surfaces to blend correctly.
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(
            gl.GL_SRC_ALPHA,
            gl.GL_ONE_MINUS_SRC_ALPHA
        )

    # ---------------------------------------------------------
    # Surfaces
    # ---------------------------------------------------------

    def make_surface(self, width, height, alpha=False):
        pygame = self.system.backend.pygame

        flags = pygame.SRCALPHA if alpha else 0

        return pygame.Surface(
            (width, height),
            flags
        )

    def load_image(self, file_like):
        return self.system.backend.pygame.image.load(file_like)

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

    def draw_overlay(self, color, alpha):
        overlay = self.make_surface(
            self.width,
            self.height,
            alpha=True
        )

        overlay.fill((*color, alpha))

        return overlay

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------

    def fill(self, color, alpha=None):
        """
        Clear the OpenGL window with a color.
        """

        color = self._normalize_color(color, alpha)

        r, g, b, a = color

        gl = self.system.backend.opengl

        gl.glClearColor(
            r / 255,
            g / 255,
            b / 255,
            a / 255
        )

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def Rect(self, *args):
        return self.system.backend.pygame.Rect(*args)

    def mask(self, surface):
        """
        Create a pixel mask from a surface.
        """

        return self.system.backend.pygame.mask.from_surface(surface)

    def draw_circle(
        self,
        surface,
        color,
        position,
        radius,
        width=0,
        object=None
    ):
        """
        Draw a circle directly with OpenGL.

        A circle is approximated using a polygon made from
        multiple points around its circumference.

        width=0 draws a filled circle.
        width>0 draws an outlined circle.
        """

        color = self._normalize_color(color)
        gl = self.system.backend.opengl
        math = self.system.math

        self._set_color(color)

        segments = max(24, int(radius * 2))

        center_x, center_y = position

        if width:
            gl.glLineWidth(width)
            gl.glBegin(gl.GL_LINE_LOOP)

            for i in range(segments):
                angle = (2 * math.pi * i) / segments

                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                gl.glVertex2f(x, y)

            gl.glEnd()

        else:
            gl.glBegin(gl.GL_TRIANGLE_FAN)

            gl.glVertex2f(center_x, center_y)

            for i in range(segments + 1):
                angle = (2 * math.pi * i) / segments

                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                gl.glVertex2f(x, y)

            gl.glEnd()
    
    def draw_rect(
        self,
        surface,
        color,
        rect,
        width=0,
        border_radius=None,
        object=None
    ):
        """
        Draw a rectangle directly with OpenGL.

        The surface argument is currently ignored because
        OpenGL draws directly to the window.
        """

        x, y, width_, height = rect

        color = self._normalize_color(color)
        gl = self.system.backend.opengl

        self._set_color(color)

        if width:
            gl.glBegin(gl.GL_LINE_LOOP)
        else:
            gl.glBegin(gl.GL_QUADS)

        gl.glVertex2f(x, y)
        gl.glVertex2f(x + width_, y)
        gl.glVertex2f(x + width_, y + height)
        gl.glVertex2f(x, y + height)

        gl.glEnd()

    def draw_line(
        self,
        surface,
        point_a,
        point_b,
        color,
        width=None
    ):
        """
        Draw a line directly with OpenGL.
        """

        color = self._normalize_color(color)
        gl = self.system.backend.opengl

        self._set_color(color)

        if width is not None:
            gl.glLineWidth(width)

        gl.glBegin(gl.GL_LINES)

        gl.glVertex2f(*point_a)
        gl.glVertex2f(*point_b)

        gl.glEnd()

    # ---------------------------------------------------------
    # OpenGL helpers
    # ---------------------------------------------------------

    def _normalize_color(self, color, alpha=None):
        """
        Convert RGB/RGBA into RGBA.
        """

        if len(color) == 3:
            alpha = 255 if alpha is None else alpha
            return (*color, alpha)

        if len(color) == 4:
            return color

        raise ValueError(
            "Color must be an RGB or RGBA tuple"
        )

    def _set_color(self, color):
        """
        Set the current OpenGL drawing color.
        """

        r, g, b, a = color

        gl = self.system.backend.opengl

        gl.glColor4f(
            r / 255,
            g / 255,
            b / 255,
            a / 255
        )

    # ---------------------------------------------------------
    # Window interface
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

    def default_fill(self):
        self.fill((0, 0, 0))

    def blit(self, surface, destination, area=None):
        pass

    def update(self):
        """
        Present everything that has been drawn this frame.
        """

        self.window.flip()

    def get_screen(self):
        return self.window

    def get_fps(self):
        return self.system.time.get_fps()

    def quit(self):
        return self.system.backend.pygame.quit()