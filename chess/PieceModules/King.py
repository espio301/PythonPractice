from PieceModules.Piece import Piece
class King(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name="King"
        self.can_catsle = True
        self.move_patterns = []
        self.set_king_move_patterns()
    
    def set_king_move_patterns(self):
        for r in range(-1,2):
            for c in range(-1,2):
                self.move_patterns.append([r,c])
        self.move_patterns.remove([0,0])

    def set_coords(self, coordinates):
        self.coordinates = coordinates
        self.can_castle = False

    def get_can_castle(self):
        return self.can_catsle

