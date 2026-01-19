from PieceModules.Piece import Piece
class King(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name="King"
        self.move_patterns = []
        self.set_king_move_patterns()
    
    def set_king_move_patterns(self):
        for r in range(-1,2):
            for c in range(-1,2):
                self.move_patterns.append([r,c])
        self.move_patterns.remove([0,0])

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()

