from OpenGL import GL as gl

import numpy

from helper import asset

from core.draw.camera import Camera3D
from core.draw.shader import Shader
from core.draw.batching.texturebatch import TextureBatch
from core.draw.geometry.line import Line


class Renderer:

    def __init__(self, window, resolution=(1600, 900)):

        self.window = window
        self.resolution = resolution
        self.camera = Camera3D()

        self.default_shader = Shader(asset("v"), asset("f"))
        self.texture_shader = Shader(asset("texturev"), asset("texturef"))

        self.texture_batch = None
        self.texture_batch_vao = None
        self.texture_batch_vbo = None
        self.texture_batch_ebo = None

        self.initialize_opengl()
        self.initialize_texture_batch()
        self.shaders = {}

    def set_res(self, resolution):

        self.resolution = resolution

    def shader(self,vertex_filename,fragment_filename):

        key = (vertex_filename,fragment_filename)

        if key not in self.shaders:
            self.shaders[key] = Shader(asset(vertex_filename),asset(fragment_filename))

        return self.shaders[key]
    
    def update_viewport(self):
        width, height = self.window.size

        self.resolution = (width, height)

        gl.glViewport(0, 0, width, height)

    def render_2d(self, object, shader, time):

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glUniform4f(
            shader.color_location,
            *object.color
        )

        gl.glUniform1f(
            shader.time_location,
            time
        )

        if hasattr(object, "border_radius") and object.border_radius is not None:

            gl.glUniform2f(
                shader.rect_size_location,
                object.width,
                object.height
            )

            gl.glUniform1f(
                shader.border_radius_location,
                object.border_radius
            )

    def render_3d(self, object, shader, time):

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glUniform4f(shader.color_location, *object.color)
        gl.glUniform1f(shader.time_location, time)

        gl.glUniformMatrix4fv(shader.model_location, 1, gl.GL_TRUE, object.model_matrix())
        gl.glUniformMatrix4fv(shader.view_location, 1, gl.GL_TRUE, self.camera.view_matrix())
        gl.glUniformMatrix4fv(shader.projection_location, 1, gl.GL_TRUE, self.camera.projection_matrix(self.window.size[0] / self.window.size[1]))

    def render_texture(self, object, shader, time):

        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glUniform1f(shader.time_location, time)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, object.texture.id)

        gl.glUniform1i(shader.texture_location, 0)

    def render(self, object, time):

        shader = object.shader or self.default_shader

        gl.glUseProgram(shader.program)

        if getattr(object, "texture", None):

            self.render_texture(object, shader, time)

        elif object.dimension == 2:

            self.render_2d(object, shader, time)

        elif object.dimension == 3:

            self.render_3d(object, shader, time)

        gl.glBindVertexArray(object.vao)

        if isinstance(object, Line):

            gl.glLineWidth(object.width)

            gl.glDrawElements(
                gl.GL_LINES,
                object.vertex_count,
                gl.GL_UNSIGNED_INT,
                None
            )

        else:

            gl.glDrawElements(
                gl.GL_TRIANGLES,
                object.vertex_count,
                gl.GL_UNSIGNED_INT,
                None
            )

    def clear(self, color=(0.0, 0.0, 0.0, 1.0)):
        width, height = self.window.size

        self.resolution = (width, height)

        gl.glViewport(0, 0, width, height)
        gl.glClearColor(*color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def initialize_opengl(self):

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def initialize_texture_batch(self):

        self.texture_batch_vao = gl.glGenVertexArrays(1)
        self.texture_batch_vbo = gl.glGenBuffers(1)
        self.texture_batch_ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.texture_batch_vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.texture_batch_vbo)

        stride = 4 * numpy.dtype(numpy.float32).itemsize

        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, None)
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, gl.ctypes.c_void_p(2 * numpy.dtype(numpy.float32).itemsize))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.texture_batch_ebo)

        gl.glBindVertexArray(0)

    def begin_texture_batch(self,texture,vshader=None,fshader=None,shadervals=None,light_surface=None):

        shader = self.texture_shader

        if vshader is not None and fshader is not None:
            shader = self.shader(vshader,fshader)

        if self.texture_batch is not None:

            if self.texture_batch.texture is texture and self.texture_batch.shader is shader:
                return

            self.flush_texture_batch()

        self.texture_batch = TextureBatch(texture,shader,shadervals,light_surface)


    def add_texture_quad(self, texture, x, y, width, height,vshader=None,fshader=None,shadervals=None,light_surface=None):

        self.begin_texture_batch(texture,vshader,fshader,shadervals,light_surface)

        rw, rh = self.resolution

        x1 = (x - width / 2) / rw * 2 - 1
        y1 = 1 - (y - height / 2) / rh * 2

        x2 = (x + width / 2) / rw * 2 - 1
        y2 = 1 - (y + height / 2) / rh * 2

        self.texture_batch.add(x1, y1, x2, y2)
        
    def flush_texture_batch(self):

        if self.texture_batch is None:
            return

        batch = self.texture_batch
        self.texture_batch = None

        vertices = numpy.array(batch.vertices, dtype=numpy.float32)
        indices = numpy.array(batch.indices, dtype=numpy.uint32)

        if len(indices) == 0:
            return

        shader = batch.shader

        gl.glUseProgram(shader.program)

        if batch.shadervals is not None:
            for location,value in zip(shader.shadervals,batch.shadervals):
                gl.glUniform1f(location,value)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glUniform1f(shader.time_location, 0.0)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, batch.texture.id)
        gl.glUniform1i(shader.texture_location, 0)

        gl.glBindVertexArray(self.texture_batch_vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.texture_batch_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_DYNAMIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.texture_batch_ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_DYNAMIC_DRAW)

        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

        gl.glBindVertexArray(0)