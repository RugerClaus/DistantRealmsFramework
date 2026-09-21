import numpy

class Rect:
    def __init__(self, x, y, w, h, vao, vbo, color=(0.5, 0.5, 0.5, 1.0),shader=None,border_radius=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = 6
        self.color = color
        self.shader = shader
        self.border_radius = border_radius
        self.dimension = 2
        self.orientation = "center"

    @property
    def position(self):
        return numpy.asarray((self.x,self.y),dtype=numpy.float32)