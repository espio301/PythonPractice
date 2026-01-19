from PieceModules.Piece import Piece
class Rook(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "rook"
        self.move_patterns = []
        self.set_rook_move_patterns()

    def set_rook_move_patterns(self):
        for i in range(-7,8):
            self.move_patterns.append([0,i])
            self.move_patterns.append([i,0])
