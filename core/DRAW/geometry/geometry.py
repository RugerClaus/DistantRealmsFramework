import numpy
import OpenGL.GL as gl
from core.DRAW.vertex import Vertex
from core.DRAW.geometry.rect import Rect
from core.DRAW.geometry.circle import Circle
from core.DRAW.geometry.cube import Cube
from core.DRAW.geometry.plane import Plane
from core.DRAW.geometry.texture import Texture
from core.DRAW.geometry.line import Line
from core.DRAW.geometry.model import Model
from core.DRAW.geometry.billboard import Billboard

class Geometry:

    renderer = None

    @classmethod
    def init(cls, renderer):
        cls.renderer = renderer

    @classmethod
    def rect(cls, x, y, w, h, color=(0.5, 0.5, 0.5, 1.0), border_radius=None, shader=None):

        rw, rh = cls.renderer.window.size

        x1 = ((x - w / 2) / rw) * 2 - 1
        y1 = 1 - ((y - h / 2) / rh) * 2

        x2 = ((x + w / 2) / rw) * 2 - 1
        y2 = 1 - ((y + h / 2) / rh) * 2

        vertices = numpy.array([
            (x1, y1, 0.0, 0.0),
            (x2, y1, 1.0, 0.0),
            (x2, y2, 1.0, 1.0),
            (x1, y2, 0.0, 1.0)
        ], dtype=numpy.float32)

        indices = numpy.array(
            [0, 1, 2, 0, 2, 3],
            dtype=numpy.uint32
        )

        vertex = Vertex(vertices, indices)
        vertex.create_data(attributes=4)

        if border_radius is not None:
            shader = cls.renderer.shader("roundedrectv", "roundedrectf")

        return Rect(x, y, w, h, vertex.vao, vertex.vbo, color, shader, border_radius)

    @classmethod
    def update_rect(cls, rect):

        rw, rh = cls.renderer.resolution

        if rect.orientation == "topleft":
            x1 = (rect.x / rw) * 2 - 1
            y1 = 1 - (rect.y / rh) * 2

            x2 = ((rect.x + rect.width) / rw) * 2 - 1
            y2 = 1 - ((rect.y + rect.height) / rh) * 2

        elif rect.orientation == "center":
            x1 = ((rect.x - rect.width / 2) / rw) * 2 - 1
            y1 = 1 - ((rect.y - rect.height / 2) / rh) * 2

            x2 = ((rect.x + rect.width / 2) / rw) * 2 - 1
            y2 = 1 - ((rect.y + rect.height / 2) / rh) * 2

        vertices = numpy.array([
            (x1, y1, 0.0, 0.0),
            (x2, y1, 1.0, 0.0),
            (x2, y2, 1.0, 1.0),
            (x1, y2, 0.0, 1.0)
        ], dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, rect.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    @classmethod
    def line(cls,x1,y1,x2,y2,color=(0.5, 0.5, 0.5, 1.0),width=1,shader=None):

        rw, rh = cls.renderer.resolution

        vertices = numpy.array([
            ((x1 / rw) * 2 - 1, 1 - (y1 / rh) * 2),
            ((x2 / rw) * 2 - 1, 1 - (y2 / rh) * 2)
        ], dtype=numpy.float32)

        indices = numpy.array(
            [0, 1],
            dtype=numpy.uint32
        )

        vertex = Vertex(vertices, indices)
        vertex.create_data()

        return Line((x1, y1),(x2, y2),width,vertex.vao,vertex.vbo,len(indices),color,shader)

    @classmethod
    def update_line(cls, line):

        rw, rh = cls.renderer.resolution

        x1, y1 = line.point_a
        x2, y2 = line.point_b

        vertices = numpy.array([
            ((x1 / rw) * 2 - 1, 1 - (y1 / rh) * 2),
            ((x2 / rw) * 2 - 1, 1 - (y2 / rh) * 2)
        ], dtype=numpy.float32)

        gl.glBindBuffer(
            gl.GL_ARRAY_BUFFER,
            line.vbo
        )

        gl.glBufferSubData(
            gl.GL_ARRAY_BUFFER,
            0,
            vertices.nbytes,
            vertices
        )

    @classmethod
    def circle(cls, centerx, centery, radius, color=(0.5, 0.5, 0.5, 1.0), shader=None, segments=64):
        rw, rh = cls.renderer.resolution

        angles = numpy.linspace(0,2 * numpy.pi,segments,endpoint=False)

        normalized_centerx = (centerx / rw) * 2 - 1
        normalized_centery = 1 - (centery / rh) * 2

        vertices = [(normalized_centerx, normalized_centery)]

        for angle in angles:
            x = centerx + radius * numpy.cos(angle)
            y = centery + radius * numpy.sin(angle)

            x = (x / rw) * 2 - 1
            y = 1 - (y / rh) * 2

            vertices.append((x, y))

        vertices = numpy.array(vertices, dtype=numpy.float32)

        indices = []

        for i in range(segments):
            indices.extend([0,i + 1,((i + 1) % segments) + 1])

        indices = numpy.array(indices, dtype=numpy.uint32)

        vertex = Vertex(vertices, indices)
        vertex.create_data()

        return Circle(centerx,centery,radius,vertex.vao,vertex.vbo,segments,len(indices),color,shader)

    @classmethod
    def update_circle(cls, circle):
        rw, rh = cls.renderer.resolution

        angles = numpy.linspace(0,2 * numpy.pi,circle.segments,endpoint=False)

        normalized_centerx = (circle.x / rw) * 2 - 1
        normalized_centery = 1 - (circle.y / rh) * 2

        vertices = [(normalized_centerx, normalized_centery)]

        for angle in angles:
            x = circle.x + circle.radius * numpy.cos(angle)
            y = circle.y + circle.radius * numpy.sin(angle)

            x = (x / rw) * 2 - 1
            y = 1 - (y / rh) * 2

            vertices.append((x, y))

        vertices = numpy.array(vertices, dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, circle.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER,0,vertices.nbytes,vertices)

    @classmethod
    def cube(cls, x, y, z, size, color=(0.5, 0.5, 0.5, 1.0), shader=None):
        vertices=numpy.array([
            # Front
            (-size/2,-size/2,-size/2,0,0,-1),
            ( size/2,-size/2,-size/2,0,0,-1),
            ( size/2, size/2,-size/2,0,0,-1),
            (-size/2, size/2,-size/2,0,0,-1),

            # Back
            (-size/2,-size/2, size/2,0,0,1),
            ( size/2,-size/2, size/2,0,0,1),
            ( size/2, size/2, size/2,0,0,1),
            (-size/2, size/2, size/2,0,0,1),

            # Left
            (-size/2,-size/2,-size/2,-1,0,0),
            (-size/2, size/2,-size/2,-1,0,0),
            (-size/2, size/2, size/2,-1,0,0),
            (-size/2,-size/2, size/2,-1,0,0),

            # Right
            (size/2,-size/2,-size/2,1,0,0),
            (size/2,-size/2, size/2,1,0,0),
            (size/2, size/2, size/2,1,0,0),
            (size/2, size/2,-size/2,1,0,0),

            # Top
            (-size/2,size/2,-size/2,0,1,0),
            ( size/2,size/2,-size/2,0,1,0),
            ( size/2,size/2, size/2,0,1,0),
            (-size/2,size/2, size/2,0,1,0),

            # Bottom
            (-size/2,-size/2,-size/2,0,-1,0),
            ( size/2,-size/2,-size/2,0,-1,0),
            ( size/2,-size/2, size/2,0,-1,0),
            (-size/2,-size/2, size/2,0,-1,0)
        ],dtype=numpy.float32)

        indices=numpy.array([
            0,1,2,0,2,3,
            4,6,5,4,7,6,
            8,9,10,8,10,11,
            12,13,14,12,14,15,
            16,17,18,16,18,19,
            20,22,21,20,23,22
        ],dtype=numpy.uint32)

        vertex = Vertex(vertices, indices)
        vertex.create_data_3d(6)

        return Cube(x, y, z,size,vertex.vao,vertex.vbo,len(indices),color,shader)

    @classmethod
    def update_cube(cls,cube):
        half=cube.size/2
        vertices=numpy.array([
            # Front
            (-half,-half,-half,0,0,-1),
            ( half,-half,-half,0,0,-1),
            ( half, half,-half,0,0,-1),
            (-half, half,-half,0,0,-1),

            # Back
            (-half,-half,half,0,0,1),
            ( half,-half,half,0,0,1),
            ( half, half,half,0,0,1),
            (-half, half,half,0,0,1),

            # Left
            (-half,-half,-half,-1,0,0),
            (-half, half,-half,-1,0,0),
            (-half, half,half,-1,0,0),
            (-half,-half,half,-1,0,0),

            # Right
            (half,-half,-half,1,0,0),
            (half,-half,half,1,0,0),
            (half, half,half,1,0,0),
            (half, half,-half,1,0,0),

            # Top
            (-half,half,-half,0,1,0),
            ( half,half,-half,0,1,0),
            ( half,half,half,0,1,0),
            (-half,half,half,0,1,0),

            # Bottom
            (-half,-half,-half,0,-1,0),
            ( half,-half,-half,0,-1,0),
            ( half,-half,half,0,-1,0),
            (-half,-half,half,0,-1,0)
        ],dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,cube.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER,0,vertices.nbytes,vertices)

    @classmethod
    def plane(cls, x, y, z, width, depth, color=(0.5, 0.5, 0.5, 1.0), shader=None):

        vertices = numpy.array([
            (-width / 2, 0.0, -depth / 2),
            ( width / 2, 0.0, -depth / 2),
            ( width / 2, 0.0,  depth / 2),
            (-width / 2, 0.0,  depth / 2)
        ], dtype=numpy.float32)

        indices = numpy.array([
            0, 1, 2,
            0, 2, 3
        ], dtype=numpy.uint32)

        vertex = Vertex(vertices, indices)
        vertex.create_data_3d()

        return Plane(
            x, y, z,
            width, depth,
            vertex.vao,
            vertex.vbo,
            len(indices),
            color,
            shader
        )

    @classmethod
    def update_plane(cls, plane):
        half_width = plane.width / 2
        half_depth = plane.depth / 2

        vertices = numpy.array([
            (-half_width, 0.0, -half_depth),
            ( half_width, 0.0, -half_depth),
            ( half_width, 0.0,  half_depth),
            (-half_width, 0.0,  half_depth)
        ], dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, plane.vbo)
        gl.glBufferSubData(
            gl.GL_ARRAY_BUFFER,
            0,
            vertices.nbytes,
            vertices
        )

    @classmethod
    def texture(cls, x, y, w, h, texture, shader=None):

        rw, rh = cls.renderer.resolution

        x1 = (x - w / 2) / rw * 2 - 1
        y1 = 1 - (y - h / 2) / rh * 2

        x2 = (x + w / 2) / rw * 2 - 1
        y2 = 1 - (y + h / 2) / rh * 2

        vertices = numpy.array([
            # position       UV
            (x1, y1,          0.0, 1.0),
            (x2, y1,          1.0, 1.0),
            (x2, y2,          1.0, 0.0),
            (x1, y2,          0.0, 0.0)
        ], dtype=numpy.float32)

        indices = numpy.array([
            0, 1, 2,
            0, 2, 3
        ], dtype=numpy.uint32)

        vertex = Vertex(vertices, indices)
        vertex.create_data_textured()

        return Texture(x,y,w,h,vertex.vao,vertex.vbo,texture,shader)

    @classmethod
    def update_texture(cls, texture):
        rw, rh = cls.renderer.resolution

        x1 = (texture.x - texture.width / 2) / rw * 2 - 1
        y1 = 1 - (texture.y - texture.height / 2) / rh * 2

        x2 = (texture.x + texture.width / 2) / rw * 2 - 1
        y2 = 1 - (texture.y + texture.height / 2) / rh * 2

        vertices = numpy.array([
            (x1, y1, 0.0, 1.0),
            (x2, y1, 1.0, 1.0),
            (x2, y2, 1.0, 0.0),
            (x1, y2, 0.0, 0.0)
        ], dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, texture.vbo)

        gl.glBufferSubData(
            gl.GL_ARRAY_BUFFER,
            0,
            vertices.nbytes,
            vertices
        )

    @classmethod
    def model(cls,x,y,z,mesh_name=None,vertices=None,faces=None,color=(0.5,0.5,0.5,1.0),shader=None):
        model=Model(vertices,faces,mesh_name,(x,y,z),color=color,shader=shader)
        indices=model.faces.flatten()
        vertex=Vertex(model.vertices,indices)
        vertex.create_data_3d(6)
        model.vao=vertex.vao
        model.vbo=vertex.vbo
        model.vertex_count=len(indices)
        return model

    @classmethod
    def update_model(cls, model):
        vertices = numpy.asarray(model.vertices, dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, model.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

    @classmethod
    def billboard(cls,x,y,z,width,height,texture,shader=None):
        vertices=numpy.array([
            (-width/2,-height/2,0.0,0.0,0.0),
            ( width/2,-height/2,0.0,1.0,0.0),
            ( width/2, height/2,0.0,1.0,1.0),
            (-width/2, height/2,0.0,0.0,1.0)
        ],dtype=numpy.float32)

        indices=numpy.array([0,1,2,0,2,3],dtype=numpy.uint32)

        vertex=Vertex(vertices,indices)
        vertex.create_data_textured_3d()

        return Billboard(x,y,z,width,height,vertex.vao,vertex.vbo,texture,shader)

    @classmethod
    def update_billboard(cls,billboard):
        width = billboard.width
        height = billboard.height

        vertices=numpy.array([
            (-width/2,-height/2,0.0,0.0,0.0),
            ( width/2,-height/2,0.0,1.0,0.0),
            ( width/2, height/2,0.0,1.0,1.0),
            (-width/2, height/2,0.0,0.0,1.0)
        ],dtype=numpy.float32)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,billboard.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER,0,vertices.nbytes,vertices)

    @classmethod
    def update(cls,objects):
        for object in objects:
            if isinstance(object,Rect):
                cls.update_rect(object)
            elif isinstance(object,Circle):
                cls.update_circle(object)
            elif isinstance(object,Cube):
                cls.update_cube(object)
            elif isinstance(object,Plane):
                cls.update_plane(object)
            elif isinstance(object,Texture):
                cls.update_texture(object)
            elif isinstance(object, Line):
                cls.update_line(object)
            elif isinstance(object,Model):
                cls.update_model(object)
            elif isinstance(object,Billboard):
                cls.update_billboard(object)