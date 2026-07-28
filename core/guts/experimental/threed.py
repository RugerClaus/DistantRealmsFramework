from core.util.experimental.math3d import rotate_x, rotate_y, rotate_z, Vec3, facing, triangle_depth
from core.util.experimental.model import load_mesh,Model
from core.util.triangle import Triangle
from core.application.camera import Camera
from core.util.colors import *



class Engine:
    def __init__(self, system, game_state):
        self.system = system
        self.game_state = game_state

        self.sphere = Model(*load_mesh("core/meshes/sphere.mesh"), Vec3(2, 0, 0))
        self.sphere2 = Model(*load_mesh("core/meshes/sphere.mesh"), Vec3(2, 5, 0))

        self.cube1 = Model(*load_mesh("core/meshes/cube.mesh"), Vec3(1, 1, -8))
        self.models = []
        self.models.append(self.sphere)
        self.models.append(self.sphere2)
        self.models.append(self.cube1)


        self.face_colors = face_colors

        self.camera = Camera(Vec3(0,0,-10), Vec3(0,0,0))
        self.polygons = []

        self.surface = self.system.window.make_surface(self.system.window.get_width(), self.system.window.get_height())


    def project(self, v):
        if v.z <= 0.1:
            return None

        f = 200
        cx = self.system.window.get_width() / 2
        cy = self.system.window.get_height() / 2

        factor = f / v.z
        return Vec3(
            v.x * factor + cx,
            v.y * factor + cy,
            v.z
        )

    def yaw(self):
        if self.system.input.is_pressed(self.system.input.keys.w_key()):
            self.camera.rotation.x += 0.05
        elif self.system.input.is_pressed(self.system.input.keys.s_key()):
            self.camera.rotation.x -= 0.05

    def pitch(self):
        if self.system.input.is_pressed(self.system.input.keys.a_key()):
            self.camera.rotation.y += 0.05
        elif self.system.input.is_pressed(self.system.input.keys.d_key()):
            self.camera.rotation.y -= 0.05

    def roll(self):
        if self.system.input.is_pressed(self.system.input.keys.e_key()):
            self.camera.rotation.z += 0.05
        elif self.system.input.is_pressed(self.system.input.keys.q_key()):
            self.camera.rotation.z -= 0.05

    def resize(self):
        self.surface = self.system.window.make_surface(self.system.window.get_width(), self.system.window.get_height())

    def handle_input(self):
        self.yaw()
        self.pitch()
        self.roll()

        # --- MOVE CAMERA FORWARD / BACK (Z) ---
        if self.system.input.is_pressed(self.system.input.keys.up_arrow_key()):
            self.camera.position.z += 0.1

        if self.system.input.is_pressed(self.system.input.keys.down_arrow_key()):
            self.camera.position.z -= 0.1

        # --- LEFT / RIGHT (X) ---
        if self.system.input.is_pressed(self.system.input.keys.left_arrow_key()):
            self.camera.position.x -= 0.1

        if self.system.input.is_pressed(self.system.input.keys.right_arrow_key()):
            self.camera.position.x += 0.1

        # --- UP / DOWN (Y) ---
        if self.system.input.is_pressed(self.system.input.keys.page_up_key()):
            self.camera.position.y += 0.1

        if self.system.input.is_pressed(self.system.input.keys.page_down_key()):
            self.camera.position.y -= 0.1
    

    def transform_vertex(self, v, model):

        v = v + model.position

        # --- CAMERA SPACE ---
        v = v - self.camera.position

        # camera rotation (inverse)
        v = rotate_x(v, -self.camera.rotation.x)
        v = rotate_y(v, -self.camera.rotation.y)
        v = rotate_z(v, -self.camera.rotation.z)

        return v

    def draw_polygons(self):
        self.surface.fill((0,0,0))
        self.polygons = []

        for model in self.models:
            for i, face in enumerate(model.faces):

                verts = []
                for idx in face:
                    v = self.transform_vertex(model.vertices[idx], model)
                    verts.append(v)
                    print(min(v.z for v in verts), max(v.z for v in verts))

                v0, v1, v2 = verts

                if not facing(v0, v1, v2):
                    continue

                tri = Triangle(v0, v1, v2, white)
                tri.fill_color = self.face_colors[i % len(self.face_colors)]
                self.polygons.append(tri)
        self.polygons.sort(key=triangle_depth, reverse=True)

        for tri in self.polygons:
            pa = self.project(tri.a)
            pb = self.project(tri.b)
            pc = self.project(tri.c)
            if pa is None or pb is None or pc is None:
                continue

            pa = (int(pa.x), int(pa.y))
            pb = (int(pb.x), int(pb.y))
            pc = (int(pc.x), int(pc.y))
            
            tri.fill_color = self.face_colors[i % len(self.face_colors)]
            self.draw_triangle(pa, pb, pc, white)

            self.draw_points(pa, pb, pc,self.face_colors[0])
            self.draw_faces(pa,pb,pc,tri.fill_color)
        
        self.system.window.blit(self.surface, (0,0))

    def draw_triangle(self, a, b, c, color):
        self.system.window.draw_line(self.surface, a, b, color)
        self.system.window.draw_line(self.surface, b, c, color)
        self.system.window.draw_line(self.surface, c, a, color)

    def draw_points(self, a, b, c, color):

        self.system.window.draw_circle(self.surface, color, a, 5)
        self.system.window.draw_circle(self.surface, color, b, 5)
        self.system.window.draw_circle(self.surface, color, c, 5)

    def draw_faces(self,a,b,c,color):
        ca, cb, cc = color

        self.system.window.draw_polygon(self.surface, (ca,cb,cc),(a,b,c))

    def run(self):
        self.handle_input()
        self.draw_polygons()
        
        