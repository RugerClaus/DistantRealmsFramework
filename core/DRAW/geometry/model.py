import numpy
from helper import asset

class Model:
    def __init__(self,vertices=None,faces=None,mesh_name=None,position=(0,0,0),vao=None,vbo=None,count=0,color=(0.5,0.5,0.5,1.0),shader=None):
        self.mesh_name=mesh_name
        self.vertices,self.faces=self.load_mesh() if mesh_name else (vertices,faces)
        self.position=numpy.asarray(position,dtype=numpy.float32)
        self.rotation=numpy.zeros(3,dtype=numpy.float32)
        self.scale=numpy.ones(3,dtype=numpy.float32)
        self.vao=vao
        self.vbo=vbo
        self.vertex_count=count
        self.color=color
        self.shader=shader
        self.dimension=3
        self.always_visible=False

    def model_matrix(self):
        matrix=numpy.eye(4,dtype=numpy.float32)
        matrix[:3,3]=self.position
        matrix[:3,:3]=numpy.diag(self.scale)
        return matrix

    def load_mesh(self):
        vertices=[]
        faces=[]

        with open(asset(self.mesh_name),"r") as f:
            for line in f:
                line=line.strip()

                if line.startswith("v "):
                    _,x,y,z,nx,ny,nz=line.split()
                    vertices.append((float(x),float(y),float(z),float(nx),float(ny),float(nz)))

                elif line.startswith("f "):
                    parts=line.split()[1:]
                    face=[]

                    for part in parts:
                        index=part.split("/")[0]
                        face.append(int(index)-1)

                    for i in range(1,len(face)-1):
                        faces.append((face[0],face[i],face[i+1]))

        return numpy.array(vertices,dtype=numpy.float32),numpy.array(faces,dtype=numpy.uint32)

    @staticmethod
    def sphere_mesh(radius=1.0, segments=32, rings=16):
        vertices=[]
        faces=[]

        for ring in range(rings+1):
            phi=numpy.pi*ring/rings
            y=numpy.cos(phi)
            ring_radius=numpy.sin(phi)

            for segment in range(segments):
                theta=2*numpy.pi*segment/segments

                x=ring_radius*numpy.cos(theta)
                z=ring_radius*numpy.sin(theta)

                vertices.append((
                    x*radius,
                    y*radius,
                    z*radius,
                    x,
                    y,
                    z
                ))

        for ring in range(rings):
            for segment in range(segments):
                next_segment=(segment+1)%segments

                a=ring*segments+segment
                b=ring*segments+next_segment
                c=(ring+1)*segments+next_segment
                d=(ring+1)*segments+segment

                if ring!=0:
                    faces.append((a,b,d))

                if ring!=rings-1:
                    faces.append((b,c,d))

        return numpy.asarray(vertices,dtype=numpy.float32),numpy.asarray(faces,dtype=numpy.uint32)