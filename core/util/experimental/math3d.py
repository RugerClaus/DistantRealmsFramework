import math

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self,other):
        return self.x*other.x+self.y*other.y+self.z*other.z

def rotate_x(v, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    y = v.y * cos_a - v.z * sin_a
    z = v.y * sin_a + v.z * cos_a
    return Vec3(v.x, y, z)

def rotate_y(v, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x = v.x * cos_a + v.z * sin_a
    z = -v.x * sin_a + v.z * cos_a
    return Vec3(x, v.y, z)

def rotate_z(v, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x = v.x * cos_a - v.y * sin_a
    y = v.x * sin_a + v.y * cos_a
    return Vec3(x, y, v.z)

def normalize(x,y):
    return (int(x*27.9),int(y*27.9))

def triangle_depth(tri):
    return max(tri.a.z, tri.b.z, tri.c.z)

def compute_normal(triangle):
    sidea = triangle.b.sub(triangle.a)
    sideb = triangle.c.sub(triangle.a)
    # cross product
    nx = sidea.y * sideb.z - sidea.z * sideb.y
    ny = sidea.z * sideb.x - sidea.x * sideb.z
    nz = sidea.x * sideb.y - sidea.y * sideb.x
    return Vec3(nx, ny, nz)

def facing(a, b, c):
    return (b - a).cross(c - a).z < 0