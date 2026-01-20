from PieceModules.Piece import Piece

class Pawn(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "pawn"
        self.move_patterns = [[1,1], [1,-1], [1,0], [2,0]]
        if color == "white":
            self.invert_move_patterns()

    def set_coords(self, coords):
        self.coordinates = coords
        self.remove_pawn_ummoved_pattern()
    
    def remove_pawn_ummoved_pattern(self):
        if [2,0] in self.move_patterns:
            self.move_patterns.remove([2,0])
        if [-2,0] in self.move_patterns:
            self.move_patterns.remove([-2,0])

    def get_exception_patterns(self):
        return [[1,1], [-1,-1], [1,-1], [-1,1]]

    def invert_move_patterns(self):
        for delta_index in range(len(self.move_patterns)):
            for i in range(2):
                self.move_patterns[delta_index][i] = self.move_patterns[delta_index][i] * -1

                

        
