# core/draw/draw.py

import threading,weakref

from queue import Queue, Empty
from concurrent.futures import Future

from core.draw.renderer import Renderer
from core.draw.geometry.geometry import Geometry
from core.draw.texture import Texture

blit_cache = {}
texture_delete_queue = []
geometry_cache = {}
surface_cache_dirty = set()
gpu_queue = Queue()

renderer = None
window = None
pygame = None

width = None
height = None


def normalize_color(color):

    if len(color) == 3:
        return (
            color[0] / 255.0,
            color[1] / 255.0,
            color[2] / 255.0,
            1.0
        )

    if len(color) == 4:
        return tuple(channel / 255.0 for channel in color)

    raise ValueError("color must contain 3 or 4 channels")


def queue_gpu_task(task):

    future = Future()
    gpu_queue.put((task, future))

    return future


def process_gpu_tasks():

    while True:

        try:
            task, future = gpu_queue.get_nowait()

        except Empty:

            break

        try:
            future.set_result(task())

        except Exception as error:

            future.set_exception(error)


def init(gl, glutils, pygame_api):

    global pygame

    pygame = pygame_api


def set_mode(system, title="Distant Realms Window", resizable=False, fullscreen=False):

    global renderer
    global window
    global width
    global height

    window = pygame.Window(
        title=title,
        size=(1600,900),
        resizable=resizable,
        fullscreen=fullscreen,
        opengl=True
    )

    renderer = Renderer(window)

    Geometry.init(renderer)

    renderer.update_viewport()

    return window


def set_icon(icon):

    window.set_icon(icon)


def clear(color=(0, 0, 0), alpha=None):

    if alpha is None:
        alpha = 255

    color = tuple(channel / 255.0 for channel in color)

    renderer.clear(color=(color[0], color[1], color[2], alpha / 255.0))

def line(surface, point_a, point_b, color, width=1):

    if isinstance(surface, pygame.Surface):

        pygame.draw.line(
            surface,
            color,
            point_a,
            point_b,
            width
        )

        surface_cache_dirty.add(id(surface))

        return

    renderer.flush_texture_batch()

    color = normalize_color(color)

    drawable = Geometry.line(
        point_a[0],
        point_a[1],
        point_b[0],
        point_b[1],
        color,
        width
    )

    renderer.render(drawable, 0.0)

def polygon(surface, color, points):

    if isinstance(surface, pygame.Surface):

        pygame.draw.polygon(
            surface,
            color,
            points
        )

        surface_cache_dirty.add(id(surface))

        return

def rect(surface, color, rect, width=0, border_radius=None, shader=None, object=None):

    if isinstance(surface, pygame.Surface):

        if border_radius is None:
            border_radius = 0

        pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
        surface_cache_dirty.add(id(surface))
        return

    renderer.flush_texture_batch()

    color = normalize_color(color)

    if object is not None:

        key = id(object)

        if key not in geometry_cache:

            geometry_cache[key] = Geometry.rect(
                rect.centerx,
                rect.centery,
                rect.width,
                rect.height,
                color,
                border_radius,
                shader
            )

        drawable = geometry_cache[key]

        Geometry.update_rect(drawable)

    else:

        drawable = Geometry.rect(
            rect.centerx,
            rect.centery,
            rect.width,
            rect.height,
            color,
            border_radius,
            shader
        )

    renderer.render(drawable, 0.0)

def is_on_screen(rect):

    width, height = window.size

    return not (
        rect.right < 0 or
        rect.left > width or
        rect.bottom < 0 or
        rect.top > height
    )

def cleanup_geometry():

    for key, entry in list(geometry_cache.items()):

        if not is_on_screen(entry.rect):

            entry.vertex.delete()
            del geometry_cache[key]

def circle(surface, color, center, radius, object=None):

    if isinstance(surface, pygame.Surface):

        pygame.draw.circle(
            surface,
            color,
            center,
            radius
        )

        surface_cache_dirty.add(id(surface))

        return

    renderer.flush_texture_batch()

    color = normalize_color(color)

    drawable = Geometry.circle(
        center[0],
        center[1],
        radius,
        color
    )

    renderer.render(drawable, 0.0)

def process_deleted_textures():

    while texture_delete_queue:

        texture = texture_delete_queue.pop()

        texture.delete()

def _delete_cached_texture(surface_ref):

    texture = blit_cache.pop(surface_ref,None)

    if texture is not None:
        texture_delete_queue.append(texture)

def get_texture(surface):

    if isinstance(surface,Texture):
        return surface

    for surface_ref,texture in list(blit_cache.items()):

        cached_surface = surface_ref()

        if cached_surface is surface:
            return texture

        if cached_surface is None:

            texture.delete()

            del blit_cache[surface_ref]

    surface_ref = weakref.ref(
        surface,
        _delete_cached_texture
    )

    texture = Texture(
        surface,
        keep_surface=False
    )

    blit_cache[surface_ref] = texture

    print(
        "NEW TEXTURE:",
        surface.get_size(),
        id(surface)
    )

    return texture

def make_surface(system, size, alpha=False):

    flags = pygame.SRCALPHA if alpha else 0

    return pygame.Surface(size, flags)


def upload_surface(surface, pygame_surface):

    return Texture(pygame_surface)

def update_surface(surface):

    if surface not in blit_cache:

        blit_cache[surface] = Texture(surface)

        return

    blit_cache[surface].update(surface)

def blit(surface,destination,area=None,vshader=None,fshader=None,shadervals=None,light_surface=None):

    if isinstance(surface,Texture):
        texture = surface

    else:
        texture = get_texture(surface)

        if id(surface) in surface_cache_dirty:
            texture.update(surface)
            surface_cache_dirty.remove(id(surface))

    if hasattr(destination,"x"):
        x = destination.centerx
        y = destination.centery
        dest_width = destination.width
        dest_height = destination.height

    else:
        x,y = destination

        dest_width = texture.width
        dest_height = texture.height

        x += dest_width / 2
        y += dest_height / 2

    if light_surface is not None:
        light_texture = get_texture(light_surface)
    else:
        light_texture = None

    renderer.add_texture_quad(
        texture,
        x,
        y,
        dest_width,
        dest_height,
        vshader,
        fshader,
        shadervals,
        light_texture
    )

def surface_fill(surface, color, rect=None, alpha=None):

    if isinstance(color, tuple) and len(color) == 4:
        color, alpha = color[:3], color[3]

    if alpha is None:
        alpha = 255

    color = tuple(int(channel / 255.0 * 255) for channel in color)

    if rect is None:
        surface.fill((*color, alpha))

    else:
        surface.fill((*color, alpha), rect)

    surface_cache_dirty.add(id(surface))

def delete_texture(surface):

    texture = blit_cache.pop(surface,None)

    if texture is not None:
        texture.delete()

def flip():

    renderer.flush_texture_batch()

    process_deleted_textures()

    print(
        "textures:",len(blit_cache),
        "gpu queue:",gpu_queue.qsize()
    )

    return window.flip()

def get_screen():

    return window

def mark_surface_dirty(surface):
    surface_cache_dirty.add(id(surface))

def quit():

    for texture in list(blit_cache.values()):
        texture.delete()

    blit_cache.clear()

    pygame.quit()