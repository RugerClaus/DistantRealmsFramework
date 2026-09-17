import OpenGL.GL as gl

class Vertex:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices
        self.vao = None
        self.vbo = None
        self.ebo = None

    def create_data(self, attributes=2):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            gl.GL_DYNAMIC_DRAW
        )

        if attributes == 2:
            stride = 2 * self.vertices.itemsize

            gl.glVertexAttribPointer(
                0,
                2,
                gl.GL_FLOAT,
                gl.GL_FALSE,
                stride,
                None
            )
            gl.glEnableVertexAttribArray(0)

        elif attributes == 4:
            stride = 4 * self.vertices.itemsize

            gl.glVertexAttribPointer(
                0,
                2,
                gl.GL_FLOAT,
                gl.GL_FALSE,
                stride,
                None
            )
            gl.glEnableVertexAttribArray(0)

            gl.glVertexAttribPointer(
                1,
                2,
                gl.GL_FLOAT,
                gl.GL_FALSE,
                stride,
                gl.ctypes.c_void_p(2 * self.vertices.itemsize)
            )
            gl.glEnableVertexAttribArray(1)

        else:
            raise ValueError(f"Unsupported vertex attribute format: {attributes}")

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            gl.GL_DYNAMIC_DRAW
        )

        gl.glBindVertexArray(0)

    def create_data_3d(self):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            gl.GL_DYNAMIC_DRAW
        )

        gl.glVertexAttribPointer(
            0,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            3 * self.vertices.itemsize,
            None
        )
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            gl.GL_DYNAMIC_DRAW
        )

    def create_data_textured(self):
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            gl.GL_DYNAMIC_DRAW
        )

        gl.glVertexAttribPointer(
            0,
            2,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            4 * self.vertices.itemsize,
            None
        )
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(
            1,
            2,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            4 * self.vertices.itemsize,
            gl.ctypes.c_void_p(2 * self.vertices.itemsize)
        )
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            gl.GL_DYNAMIC_DRAW
        )

    def delete(self):
        if self.vao is not None:
            gl.glDeleteVertexArrays(1, [self.vao])
            self.vao = None

        if self.vbo is not None:
            gl.glDeleteBuffers(1, [self.vbo])
            self.vbo = None

        if self.ebo is not None:
            gl.glDeleteBuffers(1, [self.ebo])
            self.ebo = None