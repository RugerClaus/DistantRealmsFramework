class TextureBatch:

    def __init__(self,texture,shader,shadervals=None,light_texture=None):

        self.texture = texture
        self.shader = shader
        self.shadervals = shadervals
        self.light_texture = light_texture

        self.vertices = []
        self.indices = []

    def add(self,x1,y1,x2,y2):

        index = len(self.vertices) // 4

        self.vertices.extend([
            x1,y1,0.0,1.0,
            x2,y1,1.0,1.0,
            x2,y2,1.0,0.0,
            x1,y2,0.0,0.0
        ])

        self.indices.extend([
            index,index + 1,index + 2,
            index,index + 2,index + 3
        ])