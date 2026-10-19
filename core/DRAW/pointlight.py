import numpy

class PointLight:

    def __init__(
        self,
        owner=None,
        color=(1.0,1.0,1.0),
        radius=10.0,
        intensity=1.0
    ):
        self.owner=owner
        self.position=numpy.zeros(3,dtype=numpy.float32)
        self.color=color
        self.radius=radius
        self.intensity=intensity

    def update(self):
        if self.owner is not None:
            self.position=numpy.asarray(
                self.owner.position,
                dtype=numpy.float32
            )