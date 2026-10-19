import numpy
from core.DRAW.geometry.geometry3d import Geometry3D
from core.DRAW.geometry.bounds import Bounds

class Cube(Geometry3D):
    def __init__(self, x, y, z, size, vao, vbo, vertex_count, color=(0.5, 0.5, 0.5, 1.0), shader=None):
        super().__init__(x,y,z)
        self.size = size
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = vertex_count
        self.color = color
        self.shader = shader
        self.dimension = 3
        self.name = "cube primitive"

    def get_bounds(self):
        half=self.size/2

        return Bounds(
            self.x-half,
            self.y-half,
            self.z-half,
            self.x+half,
            self.y+half,
            self.z+half
        )