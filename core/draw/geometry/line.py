class Line:

    def __init__(
        self,
        point_a,
        point_b,
        width,
        vao,
        vbo,
        vertex_count,
        color,
        shader=None
    ):
        self.point_a = point_a
        self.point_b = point_b
        self.width = width
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = vertex_count
        self.color = color
        self.shader = shader
        self.dimension = 2