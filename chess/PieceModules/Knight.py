from PieceModules.Piece import Piece
class Knight(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "knight"
        self.move_patterns = []
        self.set_knight_move_patterns()

    def set_knight_move_patterns(self):
        self.move_patterns = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()

    def get_move_patterns(self):
        super().get_move_patterns()

