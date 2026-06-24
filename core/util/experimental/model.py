from core.util.experimental.math3d import Vec3

class Model:
    def __init__(self, vertices, faces, position):
        self.vertices = vertices
        self.faces = faces
        self.position = position
        self.rotation = Vec3(0, 0, 0)

def load_mesh(path):
    vertices = []
    faces = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("v "):
                _, x, y, z = line.split()
                vertices.append(Vec3(float(x), float(y), float(z)))

            elif line.startswith("f "):
                parts = line.split()[1:]

                face = []
                for p in parts:
                    idx = p.split("/")[0]
                    face.append(int(idx) - 1)

                for i in range(1, len(face) - 1):
                    faces.append((face[0], face[i], face[i + 1]))

    return vertices, faces