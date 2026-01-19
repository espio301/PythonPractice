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

