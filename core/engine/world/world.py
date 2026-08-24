from core.engine.world.loader import MapLoader
from core.engine.world.camera import Camera
from core.engine.world.mechanics.environment.environment import Environment

class World:

    def __init__(self, system):
        self.system = system
        self.environment = None
        self.maps = []
        self.camera = Camera()
        self.map_loader = None
        
    def start_environment(self):
        self.environment = Environment(self.system)
        self.map_loader = MapLoader(self.system,self.environment)
        self.load_map_files()
        
    def load_map_files(self, filename=None):
        if self.map_loader:
            if filename:
                path = f"enginepersistence/world/{filename}.json"
            else:
                path = "enginepersistence/world/world.json"

            self.maps = self.map_loader.load(path)

    def is_map_visible(self, map):
        if map.wrap_x or map.wrap_y:
            return True

        camera_x = self.camera.x if map.camera_follow_x else 0
        camera_y = self.camera.y if map.camera_follow_y else 0

        left = map.world_x - camera_x
        right = left + map.map_width

        top = map.world_y - camera_y
        bottom = top + map.map_height

        return (
            right > 0 and
            left < 1 and
            bottom > 0 and
            top < 1
        )

    def scale(self):
        for map in self.maps:
            map.scale()

    def update(self):
        self.camera.update()
        self.environment.update()

        for map in self.maps:
            if self.is_map_visible(map):
                map.load()
                map.update()
            else:
                map.unload()

    def toggle_map_grid(self, name, color=None, width=None):
        for map in self.maps:
            print(map.name)
            if map.name == name:
                map.toggle_grid(color, width)
                
    def draw(self):
        self.environment.draw()
        for map in self.maps:
            if self.is_map_visible(map):
                map.draw(self.camera)

    def clean_up_states(self):
        self.system.clean_up_states([self.environment.season.state.state])