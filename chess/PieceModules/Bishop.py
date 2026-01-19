from PieceModules.Piece import Piece
class Bishop(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "bishop"
        self.move_patterns = []
        self.set_bishop_move_patterns()

    def set_bishop_move_patterns(self):
        for i in range(1,8):
            self.move_patterns.append([i,i])
            self.move_patterns.append([-i,-i])
            self.move_patterns.append([i,-i])
            self.move_patterns.append([-i,i])

