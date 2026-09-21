from OpenGL import GL as gl

from helper import load_file
from systemlogging import log_debug


class Shader:

    def __init__(self,vertex_filename,fragment_filename):

        vertex_source = load_file(vertex_filename)
        fragment_source = load_file(fragment_filename)

        vertex_shader = self._compile_shader(
            vertex_source,
            gl.GL_VERTEX_SHADER
        )

        fragment_shader = self._compile_shader(
            fragment_source,
            gl.GL_FRAGMENT_SHADER
        )

        self.program = self._create_program(
            vertex_shader,
            fragment_shader
        )

        self.time_location = gl.glGetUniformLocation(
            self.program,
            "time"
        )

        self.color_location = gl.glGetUniformLocation(
            self.program,
            "color"
        )


        self.rect_size_location = gl.glGetUniformLocation(
            self.program,
            "rect_size"
        )

        self.border_radius_location = gl.glGetUniformLocation(
            self.program,
            "border_radius"
        )

        self.model_location = gl.glGetUniformLocation(
            self.program,
            "model"
        )

        self.view_location = gl.glGetUniformLocation(
            self.program,
            "view"
        )

        self.projection_location = gl.glGetUniformLocation(
            self.program,
            "projection"
        )

        self.texture_location = gl.glGetUniformLocation(
            self.program,
            "texture_sampler"
        )

        self.brightness_location = gl.glGetUniformLocation(
            self.program,
            "brightness"
        )

        self.light_texture_location = gl.glGetUniformLocation(
            self.program,
            "light_texture"
        )

        self.billboard_texture_location = gl.glGetUniformLocation(
            self.program,
            "billboard_texture"
        )

        self.light_direction_location=gl.glGetUniformLocation(self.program,"light_direction")
        self.ambient_location=gl.glGetUniformLocation(self.program,"ambient")

        self.shadervals = [
            gl.glGetUniformLocation(
                self.program,
                "brightness"
            )
        ]

    def _compile_shader(self,source,shader_type):

        shader = gl.glCreateShader(shader_type)

        gl.glShaderSource(shader,source)
        gl.glCompileShader(shader)

        if not gl.glGetShaderiv(shader,gl.GL_COMPILE_STATUS):

            error = gl.glGetShaderInfoLog(shader).decode()

            log_debug(
                error=error,
                object="Renderer.self._compile_shader"
            )

            raise RuntimeError(error)

        return shader

    def _create_program(self,vertex_shader,fragment_shader):

        program = gl.glCreateProgram()

        gl.glAttachShader(program,vertex_shader)
        gl.glAttachShader(program,fragment_shader)

        gl.glLinkProgram(program)

        if not gl.glGetProgramiv(program,gl.GL_LINK_STATUS):

            error = gl.glGetProgramInfoLog(program)

            log_debug(
                error=error,
                object="Renderer.create_program"
            )

            raise RuntimeError(error)

        log_debug(
            error=f"Program: {program}",
            object="Renderer.create_program"
        )

        log_debug(
            error=f"Linked: {gl.glGetProgramiv(program,gl.GL_LINK_STATUS)}",
            object="Renderer.create_program"
        )

        log_debug(
            error=f"Validate: {gl.glGetProgramiv(program,gl.GL_VALIDATE_STATUS)}",
            object="Renderer.create_program"
        )

        log_debug(
            error=f"OpenGL error: {gl.glGetError()}",
            object="Renderer.create_program"
        )

        return program