def normalize_color(color):
    if not isinstance(color, (tuple, list)) or len(color) != 3:
        raise ValueError("color must be an RGB sequence")

    return color[0] / 255, color[1] / 255, color[2] / 255

def normalize_alpha(alpha):
    return alpha / 255