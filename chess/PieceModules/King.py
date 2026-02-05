from PieceModules.Piece import Piece
class King(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name="King"
        self.has_moved = False
        self.move_patterns = []
        self.set_king_move_patterns()
    
    def set_king_move_patterns(self):
        for r in range(-1,2):
            for c in range(-1,2):
                self.move_patterns.append([r,c])
        self.move_patterns.remove([0,0])

    def set_coords(self, coordinates):
        self.coordinates = coordinates
        self.has_moved = True

    def copy(self):
        copy_rook = super().copy()
        if self.has_moved:
            copy_rook.has_moved = True
        return copy_rook

    def get_has_moved(self):
        return self.has_moved

