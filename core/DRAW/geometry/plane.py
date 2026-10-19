import numpy
from core.DRAW.geometry.geometry3d import Geometry3D
from core.DRAW.geometry.bounds import Bounds

class Plane(Geometry3D):
    def __init__(self, x, y, z, w, d, vao, vbo, vertex_count, color=(0.5, 0.5, 0.5, 1.0),shader=None):
        super().__init__(x,y,z)
        self.width = w
        self.depth = d
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = vertex_count
        self.color = color
        self.shader = shader
        self.dimension = 3
        self.name = "plane"

    def model_matrix(self):
        matrix = numpy.identity(4, dtype=numpy.float32)

        matrix[0, 3] = self.x
        matrix[1, 3] = self.y
        matrix[2, 3] = self.z

        return matrix

    def get_bounds(self):
        return Bounds(
            self.x-self.width/2,
            self.y,
            self.z-self.depth/2,
            self.x+self.width/2,
            self.y,
            self.z+self.depth/2
        )