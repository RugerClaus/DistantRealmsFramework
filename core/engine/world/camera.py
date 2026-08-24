class Camera:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.target = None

    def follow(self, entity):
        self.target = entity

    def update(self):
        if self.target is None:
            return

        self.x = self.target.world_x
        self.y = self.target.world_y