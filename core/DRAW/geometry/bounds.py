class Bounds:
    def __init__(self,min_x,min_y,min_z,max_x,max_y,max_z):
        self.min=(min_x,min_y,min_z)
        self.max=(max_x,max_y,max_z)

    def intersects(self,other):
        return (
            self.min[0] <= other.max[0] and self.max[0] >= other.min[0] and
            self.min[1] <= other.max[1] and self.max[1] >= other.min[1] and
            self.min[2] <= other.max[2] and self.max[2] >= other.min[2]
        )