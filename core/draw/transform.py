import systemlogging
from core.draw.surface import Surface


def scale(original_surface, size):

    if not isinstance(size, tuple):
        systemlogging.log_warning(
            "size must be a tuple",
            "draw.transform.scale(original_surface,size=())"
        )
        return None

    if len(size) != 2:
        systemlogging.log_warning(
            "size must contain width and height",
            "draw.transform.scale(original_surface,size=(width,height))"
        )
        return None

    width, height = size

    if not isinstance(width, int) or not isinstance(height, int):
        systemlogging.log_warning(
            "size values must be integers",
            "draw.transform.scale(original_surface,size=(width,height))"
        )
        return None

    scaled_surface = Surface(
        original_surface.system,
        size,
        original_surface.alpha
    )

    # actual scaling operation here

    return scaled_surface