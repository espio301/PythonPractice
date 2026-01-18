from PieceModules.Piece import Piece
class King(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name="King"

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()