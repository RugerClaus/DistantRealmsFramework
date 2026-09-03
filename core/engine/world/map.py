from helper import sine
from core.util.colors import *
from core.engine.world.cell import Cell
from core.engine.world.mapdef import MapDef


class Map:

    def __init__(self, system, scale, environment=None,cell_data_map=None):
        self.system = system
        self.name = None
        self.z_index = 0
        self.cell_map = []
        self.cells = []
        self.cell_positions = []
        self.grid_scale = scale
        self.scale()
        self.cell_data_map = cell_data_map or {}
        self.world_x = 0
        self.world_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.camera_follow_x = False
        self.camera_follow_y = False
        self.wrap_x = False
        self.wrap_y = False
        self.map_width = 1
        self.map_height = 1
        self.draw_grid = False
        self.grid_color = white
        self.grid_line_width = 1
        self.environment = environment

        # Main rendered map layer.
        self.layer_surface = None
        self.layer_size = None
        self.layer_dirty = True

        # Cached debug grid.
        self.grid_surface = None
        self.grid_size = None
        self.grid_dirty = True

        self.map_def = MapDef()
        self.lighting_levels = 16
        self.lighting_level = 0
        self.light_layers = []

    @property
    def world_width(self):
        return self.map_width

    @property
    def world_height(self):
        return self.map_height

    @property
    def total_columns(self):
        return self.columns * self.map_width

    @property
    def total_rows(self):
        return self.rows * self.map_height

    def set_cell(self, column, row, cell_id):
        if column < 0 or column >= self.columns:
            return

        if row < 0 or row >= self.rows:
            return

        if cell_id not in self.cell_data_map:
            raise ValueError(f"Unknown cell type: {cell_id}")

        self.cell_map[row][column] = cell_id

        self.load_cells(self.cell_map)

        self.layer_dirty = True

    def get_cell_rect(self, column, row):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        left = round(column * ww / self.columns)
        right = round((column + 1) * ww / self.columns)
        top = round(row * wh / self.rows)
        bottom = round((row + 1) * wh / self.rows)
        return self.system.window.Rect(left, top, right - left, bottom - top)

    def load(self):
        if self.cells:
            return
        self.load_cells(self.cell_map)
        self.create_layer_surface()

    def unload(self):
        self.cells.clear()
        self.cell_positions.clear()
        self.layer_surface = None
        self.layer_size = None
        self.layer_dirty = True
        self.grid_surface = None
        self.grid_size = None
        self.grid_dirty = True

    def create_layer_surface(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        layer_width = round(ww * self.map_width)
        layer_height = round(wh * self.map_height)
        self.layer_surface = self.system.window.make_surface(layer_width, layer_height, True)
        self.layer_size = (layer_width, layer_height)
        self.layer_dirty = True

        # The grid must have the same dimensions as the layer.
        self.grid_dirty = True

    def create_grid_surface(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        grid_width = round(ww * self.map_width)
        grid_height = round(wh * self.map_height)
        self.grid_surface = self.system.window.make_surface(grid_width, grid_height, True)
        self.grid_size = (grid_width, grid_height)
        self.grid_surface.fill((0, 0, 0, 0))
        self.grid_dirty = True

    def render_layer(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        layer_size = (round(ww * self.map_width), round(wh * self.map_height))

        if self.layer_surface is None or self.layer_size != layer_size:
            self.create_layer_surface()

        if not self.layer_dirty:
            return
        
        self.layer_surface.fill((0, 0, 0, 0))

        for cell, (column, row) in zip(self.cells, self.cell_positions):
            rect = self.get_cell_rect(column, row)
            if cell.color:
                print("CELL COLOR:", repr(cell.color), type(cell.color))
                self.layer_surface.fill(cell.color, rect)

        self.layer_dirty = False

    def render_debug_grid(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        grid_size = (round(ww * self.map_width), round(wh * self.map_height))

        if self.grid_surface is None or self.grid_size != grid_size:
            self.create_grid_surface()

        if not self.grid_dirty:
            return

        self.grid_surface.fill((0, 0, 0, 0))
        color = self.grid_color or white
        width = self.grid_line_width or 1

        for column in range(self.columns + 1):
            x = round(column * ww / self.columns)
            self.system.window.draw_line(self.grid_surface, (x, 0), (x, wh), color, width)

        for row in range(self.rows + 1):
            y = round(row * wh / self.rows)
            self.system.window.draw_line(self.grid_surface, (0, y), (ww, y), color, width)

        self.grid_dirty = False

    def scale(self, scale=None):
        if scale is not None:
            scale = int(scale)
        else:
            scale = int(self.grid_scale)

        if scale < 1:
            raise ValueError("Map scale must be >= 1")

        self.grid_scale = scale
        self.rows = 9 * scale
        self.columns = 16 * scale
        self.grid_dirty = True

    def update_cell_colors(self):
        if self.environment is None:
            return

        brightness = self.environment.day_cycle.brightness
        level = int(brightness * (self.lighting_levels - 1))
        level = max(0, min(self.lighting_levels - 1, level))

        if level == self.lighting_level:
            return

        self.lighting_level = level

        for cell in self.cells:
            if not cell.properties.get("receives_light", False):
                continue
            cell.set_lighting_level(level)

        self.layer_dirty = True

    def update(self):
        dt = self.system.time.delta_time()
        self.world_x += self.velocity_x * dt
        self.world_y += self.velocity_y * dt
        self.update_cell_colors()

        for cell in self.cells:
            cell.update()

    def draw(self, camera=None):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()
        self.render_layer()

        if self.draw_grid:
            self.render_debug_grid()

        camera_x = camera.x if camera is not None else 0
        camera_y = camera.y if camera is not None else 0

        # World position -> screen position.
        screen_x = self.world_x * ww
        screen_y = self.world_y * wh

        # Camera influence is independent per axis.
        if self.camera_follow_x and camera is not None:
            screen_x -= camera_x * ww

        if self.camera_follow_y and camera is not None:
            screen_y -= camera_y * wh

        layer_width = self.layer_surface.get_width()
        layer_height = self.layer_surface.get_height()

        # ---------------------------------------------------------
        # X DRAWING
        # ---------------------------------------------------------

        if self.wrap_x:
            base_x = screen_x % layer_width
            x_positions = [base_x - layer_width, base_x, base_x + layer_width]
        else:
            x_positions = [screen_x]

        # ---------------------------------------------------------
        # Y DRAWING
        # ---------------------------------------------------------

        if self.wrap_y:
            base_y = screen_y % layer_height
            y_positions = [base_y - layer_height, base_y, base_y + layer_height]
        else:
            y_positions = [screen_y]

        # ---------------------------------------------------------
        # DRAW
        # ---------------------------------------------------------

        for x in x_positions:
            for y in y_positions:
                if x + layer_width < 0:
                    continue

                if x > ww:
                    continue

                if y + layer_height < 0:
                    continue

                if y > wh:
                    continue

                position = (round(x), round(y))
                self.system.window.blit(self.layer_surface, position)

                if self.draw_grid:
                    self.system.window.blit(self.grid_surface, position)

    def toggle_grid(self, grid_color=None, grid_line_width=None):
        if grid_color is not None:
            self.grid_color = grid_color

        if grid_line_width is not None:
            self.grid_line_width = grid_line_width

        self.draw_grid = not self.draw_grid
        self.grid_dirty = True
        print("toggling debug grid:", self.draw_grid, " ", self.name)

    def _get_cell_data(self, cell_type):
        return self.cell_data_map.get(cell_type)

    def load_cells(self, cell_map):
        self.cells.clear()
        self.cell_positions.clear()

        if not cell_map:
            raise ValueError("Map cannot be empty")

        source_rows = len(cell_map)
        source_columns = len(cell_map[0])

        if any(len(row) != source_columns for row in cell_map):
            raise ValueError("All map rows must have the same length")

        if source_rows != self.rows or source_columns != self.columns:
            cell_map = self.scale_map(cell_map)

        if len(cell_map) != self.rows:
            raise ValueError(f"Expected {self.rows} rows, got {len(cell_map)}")

        if len(cell_map[0]) != self.columns:
            raise ValueError(f"Expected {self.columns} columns, got {len(cell_map[0])}")

        self.cell_map = cell_map
        cell_width = 1 / self.columns
        cell_height = 1 / self.rows

        for y, row in enumerate(cell_map):
            for x, cell_id in enumerate(row):
                if cell_id == 0:
                    continue

                cell_data = self._get_cell_data(cell_id)

                if cell_data is None:
                    raise ValueError(f"Unknown cell type: {cell_id}")

                position = ((x + 0.5) * cell_width, (y + 0.5) * cell_height)
                size = (cell_width, cell_height)
                cell = Cell(self.system, size, position, cell_data)

                if cell.properties.get("receives_light", False):
                    cell.create_light_variants(self.lighting_levels)

                cell.set_lighting_level(self.lighting_level or 0)
                self.cells.append(cell)
                self.cell_positions.append((x, y))

        self.layer_dirty = True

    def scale_map(self, cell_map):
        scaled = []
        source_rows = len(cell_map)

        if source_rows == 0:
            raise ValueError("Cannot scale an empty map")

        source_columns = len(cell_map[0])

        if source_columns == 0:
            raise ValueError("Cannot scale an empty map")

        if any(len(row) != source_columns for row in cell_map):
            raise ValueError("All map rows must have the same length")

        scale = int(self.grid_scale)

        for row in cell_map:
            expanded_row = []

            for cell in row:
                expanded_row.extend([cell] * scale)

            for _ in range(scale):
                scaled.append(expanded_row.copy())

        return scaled