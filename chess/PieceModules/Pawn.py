from PieceModules.Piece import Piece

class Pawn(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "pawn"
        self.move_patterns = [[1,1], [1,-1], [1,0], [2,0]]
        if color == "white":
            self.invert_move_patterns()
        self.move_history = [coordinates]
        self.ranks_moved = 0

    def set_coords(self, coords):
        past_coords = self.coordinates
        self.ranks_moved += abs(past_coords[0]-coords[0])
        self.coordinates = coords
        self.remove_pawn_ummoved_pattern()
        self.move_history.append(coords)

    def remove_pawn_ummoved_pattern(self):
        if [2,0] in self.move_patterns:
            self.move_patterns.remove([2,0])
        if [-2,0] in self.move_patterns:
            self.move_patterns.remove([-2,0])

    def get_ranks_moved(self):
        return self.ranks_moved

    def get_exception_patterns(self):
        if self.color == "white":
            return [[-1,1],[-1,-1]]
        else:
            return [[1,-1],[1,1]]

    def invert_move_patterns(self):
        for delta_index in range(len(self.move_patterns)):
            for i in range(2):
                self.move_patterns[delta_index][i] = self.move_patterns[delta_index][i] * -1

                

        
