class Circle:
    def __init__(self, x, y, radius, vao, vbo, segments, vertex_count, color=(0.5, 0.5, 0.5, 1.0), shader=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.vao = vao
        self.vbo = vbo
        self.segments = segments
        self.vertex_count = vertex_count
        self.color = color
        self.shader = shader
        self.dimension = 2