class Texture:
    def __init__(self, x, y, w, h, vao, vbo, texture,shader=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = 6
        self.texture = texture
        self.shader = shader
        self.dimension = 2
        self.orientation = "center"
        self.color = (0.0,0.0,0.0,1.0)
