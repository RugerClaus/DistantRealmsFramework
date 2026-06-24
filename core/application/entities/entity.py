# if i ever want to mess with global entities

from core.game.entities.type import EntityType

class Entity:
    def __init__(self, x, y, board_surface, type: EntityType, size=None):
        self.x = x
        self.y = y
        self.type = type
        self.size = size
        self.board_surface = board_surface

    def update(self):
        pass

    def draw(self):
        pass