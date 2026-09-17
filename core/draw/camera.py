import numpy

class Camera3D:

    def __init__(self,fov=60.0,near=0.1,far=1000.0):
        self.fov = fov
        self.near = near
        self.far = far

        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.position = numpy.array([0.0, 0.0, 3.0], dtype=numpy.float32)

    def view_matrix(self):

        yaw = numpy.radians(self.yaw)
        pitch = numpy.radians(self.pitch)
        roll = numpy.radians(self.roll)

        cy = numpy.cos(yaw)
        sy = numpy.sin(yaw)

        cp = numpy.cos(pitch)
        sp = numpy.sin(pitch)

        cr = numpy.cos(roll)
        sr = numpy.sin(roll)

        yaw_matrix = numpy.array([
            [cy, 0.0, sy, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-sy, 0.0, cy, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=numpy.float32)

        pitch_matrix = numpy.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, cp, -sp, 0.0],
            [0.0, sp, cp, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=numpy.float32)

        roll_matrix = numpy.array([
            [cr, -sr, 0.0, 0.0],
            [sr, cr, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=numpy.float32)

        rotation = pitch_matrix @ yaw_matrix  @ roll_matrix

        translation = numpy.identity(4, dtype=numpy.float32)

        translation[0, 3] = -self.position[0]
        translation[1, 3] = -self.position[1]
        translation[2, 3] = -self.position[2]

        return rotation @ translation

    def projection_matrix(self, aspect):

        fov = numpy.radians(self.fov)

        f = 1.0 / numpy.tan(fov / 2.0)

        matrix = numpy.zeros((4, 4), dtype=numpy.float32)

        matrix[0, 0] = f / aspect
        matrix[1, 1] = f
        matrix[2, 2] = (self.far + self.near) / (self.near - self.far)
        matrix[2, 3] = (2.0 * self.far * self.near) / (self.near - self.far)
        matrix[3, 2] = -1.0

        return matrix