from PieceModules.Piece import Piece
class Rook(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "rook"
        self.move_patterns = []
        self.set_rook_move_patterns()
        print("here:", self.move_patterns)

    def set_rook_move_patterns(self):
        print("hi")
        for i in range(-7,8):
            self.move_patterns.append([0,i])
            self.move_patterns.append([i,0])
        print(self.move_patterns)
        print("bye")

    def set_coords(self, coords):
        super().set_coords(coords)

    def to_string(self):
        return super().to_string()

    def get_color(self):
        return super().get_color()
