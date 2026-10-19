import numpy
from core.DRAW.geometry.geometry3d import Geometry3D
from core.DRAW.geometry.bounds import Bounds

class Billboard(Geometry3D):
    def __init__(self,x,y,z,width,height,vao,vbo,texture,shader=None):
        super().__init__(x,y,z)
        self.width=width
        self.height=height
        self.vao=vao
        self.vbo=vbo
        self.texture=texture
        self.shader=shader
        self.vertex_count=6
        self.dimension=3
        self.billboard=True
        self.name = "billboard"

    def model_matrix(self,camera):
        direction=camera.position-numpy.array([self.x,self.y,self.z],dtype=numpy.float32)
        angle=numpy.arctan2(direction[0],direction[2])
        c=numpy.cos(angle)
        s=numpy.sin(angle)
        return numpy.array([
            [c,0,s,self.x],
            [0,1,0,self.y],
            [-s,0,c,self.z],
            [0,0,0,1]
        ],dtype=numpy.float32)

    def get_bounds(self):
        return Bounds(
            self.x-self.width/2,
            self.y-self.height/2,
            self.z,
            self.x+self.width/2,
            self.y+self.height/2,
            self.z
        )