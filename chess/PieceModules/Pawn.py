from PieceModules.Piece import Piece

class Pawn(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "pawn"
        self.move_patterns = [[1,1], [1,-1], [1,0], [2,0]]
        if color == "white":
            self.invert_move_patterns()

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        self.coordinates = coords
        self.remove_pawn_ummoved_pattern()
    
    def remove_pawn_ummoved_pattern(self):
        if [2,0] in self.move_patterns:
            self.move_patterns.remove([2,0])
        if [-2,0] in self.move_patterns:
            self.move_patterns.remove([-2,0])

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()

    def get_move_patterns(self):
        super().get_move_patterns()

    def is_valid_move_pattern(self, destination):
        movement_delta = []
        for i in range(2):
            movement_delta.append(destination[i] - self.coordinates[i])
        if movement_delta in self.move_patterns:
            return True
        return False
    
    def invert_move_patterns(self):
        for delta_index in range(len(self.move_patterns)):
            for i in range(2):
                self.move_patterns[delta_index][i] = self.move_patterns[delta_index][i] * -1

                

        
