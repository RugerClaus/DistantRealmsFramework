from core.ui.widgets.image import Image


class TextureAtlas:

    def __init__(self, system, id, image, columns, rows):
        self.system = system
        self.id = id
        self.image = Image(system, id, image)

        self.columns = columns
        self.rows = rows

        self.cell_width = self.image.original_surf.get_width() // columns
        self.cell_height = self.image.original_surf.get_height() // rows

        self.cells = []

        self.load()

    def load(self):
        for row in range(self.rows):
            for column in range(self.columns):
                rect = (column * self.cell_width,row * self.cell_height,self.cell_width,self.cell_height)

                self.cells.append(self.image.original_surf.subsurface(rect).copy())

    def get(self, index):
        return self.cells[index]

    def __len__(self):
        return len(self.cells)