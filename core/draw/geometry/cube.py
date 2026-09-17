import numpy

class Cube:
    def __init__(self, x, y, z, size, vao, vbo, vertex_count, color=(0.5, 0.5, 0.5, 1.0), shader=None):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = vertex_count
        self.color = color
        self.shader = shader
        self.dimension = 3


    def model_matrix(self):
        matrix = numpy.identity(4, dtype=numpy.float32)

        matrix[0, 3] = self.x
        matrix[1, 3] = self.y
        matrix[2, 3] = self.z

        return matrix