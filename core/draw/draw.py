# draw.draw.py
import threading
from core.draw.color import *
from core.draw.surface import Surface
import core.draw.transform as transform
from core.draw.font import Font
from queue import Queue,Empty
from concurrent.futures import Future

gpu_queue = Queue()
opengl = None
glu = None
window = None
surface = None
pygame = None
width = None
height = None

def queue_gpu_task(task):
    future = Future()
    gpu_queue.put((task, future))
    return future

def process_gpu_tasks():
    while True:
        try:
            task,future = gpu_queue.get_nowait()
        except Empty:
            break

        try:
            future.set_result(task())
        except Exception as error:
            future.set_exception(error)

def circle(a,b,c,d,e):
    pass

def create_mask(surface):
    if not hasattr(surface, "pygame_surface"):
        return None

    return pygame.mask.from_surface(surface.pygame_surface)

def mask(surface):
    if surface.mask is None and hasattr(surface, "pygame_surface"):
        surface.mask = pygame.mask.from_surface(surface.pygame_surface)

    return surface.mask

def init(gl, glutils, pygame_api):
    global opengl, glu, pygame
    opengl = gl
    glu = glutils
    pygame = pygame_api


def set_mode(system, ww, wh, title="Distant Realms Window", resizable=False, fullscreen=False):
    global window, surface, width, height

    width = ww
    height = wh

    window = pygame.Window(title=title, size=(width, height), resizable=resizable, fullscreen=fullscreen, opengl=True)

    opengl.glViewport(0, 0, width, height)

    opengl.glMatrixMode(opengl.GL_PROJECTION)
    opengl.glLoadIdentity()

    glu.gluOrtho2D(0, width, height, 0)

    opengl.glMatrixMode(opengl.GL_MODELVIEW)
    opengl.glLoadIdentity()

    surface = Surface(system, (width, height), screen=True)

    return window


def rect(surface, color, rect, width=0, border_radius=None, object=None):
    previous = opengl.glGetIntegerv(opengl.GL_FRAMEBUFFER_BINDING)

    opengl.glBindFramebuffer(
        opengl.GL_FRAMEBUFFER,
        surface.framebuffer
    )

    opengl.glDisable(opengl.GL_TEXTURE_2D)
    opengl.glDisable(opengl.GL_BLEND)

    r, g, b = normalize_color(color)
    opengl.glColor3f(r, g, b)

    opengl.glMatrixMode(opengl.GL_PROJECTION)
    opengl.glLoadIdentity()

    glu.gluOrtho2D(
        0,
        surface.size[0],
        surface.size[1],
        0
    )

    opengl.glMatrixMode(opengl.GL_MODELVIEW)
    opengl.glLoadIdentity()

    opengl.glBegin(opengl.GL_QUADS)

    opengl.glVertex2f(rect.x, rect.y)
    opengl.glVertex2f(rect.x + rect.width, rect.y)
    opengl.glVertex2f(rect.x + rect.width, rect.y + rect.height)
    opengl.glVertex2f(rect.x, rect.y + rect.height)

    opengl.glEnd()

    opengl.glBindFramebuffer(
        opengl.GL_FRAMEBUFFER,
        previous
    )


def set_icon(icon):
    pass


def clear(color, alpha):
    r, g, b = normalize_color(color)

    if alpha is not None:
        alpha = normalize_alpha(alpha)
    else:
        alpha = 1.0

    opengl.glClearColor(r, g, b, alpha)
    opengl.glClear(opengl.GL_COLOR_BUFFER_BIT)


def surface_fill(surface, color, rect=None, alpha=None):
    if isinstance(color, tuple) and len(color) == 4:
        color, alpha = color[:3], color[3]
    elif isinstance(color, tuple) and len(color) == 3:
        alpha = alpha if alpha is not None else 255

    r, g, b = normalize_color(color)

    if alpha is None:
        alpha = 1.0
    else:
        alpha = normalize_alpha(alpha)

    previous = opengl.glGetIntegerv(opengl.GL_FRAMEBUFFER_BINDING)

    opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, surface.framebuffer)

    opengl.glClearColor(r, g, b, alpha)

    if rect is None:
        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT)
    else:
        opengl.glDisable(opengl.GL_TEXTURE_2D)
        opengl.glDisable(opengl.GL_BLEND)

        opengl.glMatrixMode(opengl.GL_PROJECTION)
        opengl.glLoadIdentity()
        glu.gluOrtho2D(0, surface.size[0], surface.size[1], 0)

        opengl.glMatrixMode(opengl.GL_MODELVIEW)
        opengl.glLoadIdentity()

        opengl.glColor4f(r, g, b, alpha)

        opengl.glBegin(opengl.GL_QUADS)
        opengl.glVertex2f(rect.x, rect.y)
        opengl.glVertex2f(rect.x + rect.width, rect.y)
        opengl.glVertex2f(rect.x + rect.width, rect.y + rect.height)
        opengl.glVertex2f(rect.x, rect.y + rect.height)
        opengl.glEnd()

    opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, previous)

def upload_surface(surface, pygame_surface):
    data = pygame.image.tostring(pygame_surface, "RGBA", True)

    opengl.glBindTexture(opengl.GL_TEXTURE_2D, surface.texture)

    opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, opengl.GL_LINEAR)
    opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, opengl.GL_LINEAR)

    opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, opengl.GL_RGBA, surface.size[0], surface.size[1], 0, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE, data)

    opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

def make_surface(system,size,alpha=False):
    if threading.current_thread() is threading.main_thread():
        return Surface(system,size,alpha)

    future = queue_gpu_task(lambda: Surface(system,size,alpha))
    return future.result()


def create_surface(surface):

    width, height = surface.size
    print("GL MAX TEXTURE SIZE:", opengl.glGetIntegerv(opengl.GL_MAX_TEXTURE_SIZE))
    print("ERROR BEFORE:", opengl.glGetError())
    surface.texture = opengl.glGenTextures(1)
    print("TEXTURE:", surface.texture, "ERROR:", opengl.glGetError())
    surface.framebuffer = opengl.glGenFramebuffers(1)
    print("FBO:", surface.framebuffer, "ERROR:", opengl.glGetError())

    # create texture
    opengl.glBindTexture(opengl.GL_TEXTURE_2D, surface.texture)

    opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, opengl.GL_RGBA, width, height, 0, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE, None)

    opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, opengl.GL_LINEAR)
    opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, opengl.GL_LINEAR)

    # create framebuffer
    opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, surface.framebuffer)

    opengl.glFramebufferTexture2D(opengl.GL_FRAMEBUFFER, opengl.GL_COLOR_ATTACHMENT0, opengl.GL_TEXTURE_2D, surface.texture, 0)

    status = opengl.glCheckFramebufferStatus(opengl.GL_FRAMEBUFFER)

    if status != opengl.GL_FRAMEBUFFER_COMPLETE:
        print("FBO STATUS:", hex(status))
        print("SIZE:", width, height)
        print("TEXTURE:", surface.texture)
        print("FRAMEBUFFER:", surface.framebuffer)
        raise RuntimeError("Surface framebuffer is incomplete")

    opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, 0)


def blit(surface, destination, area=None):
    if hasattr(destination, "x"):
        x = destination.x
        y = destination.y
        dest_width = destination.width
        dest_height = destination.height
    else:
        x, y = destination
        dest_width = surface.size[0]
        dest_height = surface.size[1]

    opengl.glMatrixMode(opengl.GL_PROJECTION)
    opengl.glLoadIdentity()

    glu.gluOrtho2D(0, width, height, 0)

    opengl.glMatrixMode(opengl.GL_MODELVIEW)
    opengl.glLoadIdentity()

    opengl.glEnable(opengl.GL_TEXTURE_2D)
    opengl.glEnable(opengl.GL_BLEND)

    opengl.glBlendFunc(opengl.GL_SRC_ALPHA, opengl.GL_ONE_MINUS_SRC_ALPHA)

    opengl.glBindTexture(opengl.GL_TEXTURE_2D, surface.texture)

    opengl.glColor4f(1.0, 1.0, 1.0, 1.0)

    opengl.glBegin(opengl.GL_QUADS)

    opengl.glTexCoord2f(0.0, 1.0)
    opengl.glVertex2f(x, y)

    opengl.glTexCoord2f(1.0, 1.0)
    opengl.glVertex2f(x + dest_width, y)

    opengl.glTexCoord2f(1.0, 0.0)
    opengl.glVertex2f(x + dest_width, y + dest_height)

    opengl.glTexCoord2f(0.0, 0.0)
    opengl.glVertex2f(x, y + dest_height)

    opengl.glEnd()

    opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

    opengl.glDisable(opengl.GL_BLEND)
    opengl.glDisable(opengl.GL_TEXTURE_2D)


def flip():
    return window.flip()


def get_screen():
    return surface


def quit():
    pygame.quit()