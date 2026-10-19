import numpy

class Geometry3D:
    def __init__(self,x=0,y=0,z=0):
        self.position=numpy.asarray((x,y,z),dtype=numpy.float32)
        self.collidable=False
        self.light = None

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self,value):
        self.position[0]=value

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self,value):
        self.position[1]=value

    @property
    def z(self):
        return self.position[2]

    @z.setter
    def z(self,value):
        self.position[2]=value