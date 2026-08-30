import json,os

from core.engine.world.map import Map

class MapLoader:

    def __init__(self, system, environment):
        self.system = system
        self.environment = environment
        self.def_loader = CellDefinitionLoader()

    def load(self, index_path):
        with open(index_path, "r") as file:
            index = json.load(file)

        maps = []

        base_path = os.path.dirname(index_path)

        for entry in index.get("maps", []):
            filename = entry["file"]
            filepath = os.path.join(base_path, filename)

            with open(filepath, "r") as file:
                cell_map = [
                    [
                        int(cell)
                        for cell in line.strip().strip("[],").split(",")
                    ]
                    for line in file
                    if line.strip()
                ]

            scale = len(cell_map[0]) / 16

            cell_palette = self.def_loader.load(
                os.path.join(
                    base_path,
                    index["cell_palette"]
                )
            )

            map = Map(
                self.system,
                scale,
                self.environment,
                cell_palette
            )

            map.name = os.path.splitext(filename)[0]

            map.z = entry.get("z", 0)

            map.map_def.map_width = entry.get("width", 1)
            map.map_def.map_height = entry.get("height", 1)

            velocity = entry.get("velocity", [0, 0])

            map.velocity_x = velocity[0]
            map.velocity_y = velocity[1]

            map.camera_follow_x = entry.get("camera_follow_x", False)
            map.camera_follow_y = entry.get("camera_follow_y", False)

            map.wrap_x = entry.get("wrap_x", False)
            map.wrap_y = entry.get("wrap_y", False)

            map.world_x = entry.get("world_x",0)
            map.world_y = entry.get("world_y",0)

            map.load_cells(cell_map)
            map.create_layer_surface()

            maps.append(map)

        maps.sort(key=lambda map: map.z)

        return maps

class CellDefinitionLoader:

    def load(self, filename):

        with open(filename, "r") as file:
            definitions = json.load(file)

        definitions = definitions.get("cell_map", {})

        return {
            int(cell_id): data
            for cell_id, data in definitions.items()
        }