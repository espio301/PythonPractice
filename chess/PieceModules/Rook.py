from PieceModules.Piece import Piece
class Rook(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "rook"
        self.has_moved = False
        self.move_patterns = []
        self.set_rook_move_patterns()

    def set_rook_move_patterns(self):
        for i in range(-7,8):
            self.move_patterns.append([0,i])
            self.move_patterns.append([i,0])

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