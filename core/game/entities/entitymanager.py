import random
from core.game.entities.type import EntityType

class EntityManager:
    def __init__(self, system):
        self.system = system
        self.entities = {}

        self.reset_spawn_timers()

    def reset_entities(self):
        self.entities = {}

    def reset_spawn_timers(self):
        pass

    def add_entity(self, entity_type, sub_type=None):
        if sub_type is None:
            if entity_type == EntityType:#EntityType.entitytype
                pass
                
            elif entity_type == EntityType:#EntityType.entitytype
                pass

        else:
            pass

    def update_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.update()

    def draw_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.draw()

    def get_active_entities(self):
        active_entities = []
        for entity_list in self.entities.values():
            active_entities.extend(entity_list)
        return active_entities
    
    def check_collisions(self):
        for entity in self.get_active_entities():
            if entity.rect.colliderect(entity.rect):
                pass

    # ENTITY SPAWN METHODS BELOW