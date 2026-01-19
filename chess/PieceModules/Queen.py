from PieceModules.Piece import Piece
from PieceModules.Bishop import Bishop
from PieceModules.Rook import Rook

class Queen(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "Queen"
        self.move_patterns = []
        self.set_queen_move_patterns()

    def set_queen_move_patterns(self):
        bishop_patterns = Bishop("white", [0,0]).get_move_patterns()
        rook_patterns = Rook("white", [0,0]).get_move_patterns()
        for i in bishop_patterns:
            self.move_patterns.append(i)
        for i in rook_patterns:
            self.move_patterns.append(i)

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()

    def is_valid_move_pattern(self, destination):
        super().is_valid_move_pattern(destination)
