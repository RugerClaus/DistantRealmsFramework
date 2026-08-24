class MapDef:

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height

    @property
    def map_columns(self):
        return 16 * self.width

    @property
    def map_rows(self):
        return 9 * self.height