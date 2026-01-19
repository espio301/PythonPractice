from PieceModules.Piece import Piece
class Bishop(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)
        self.name = "bishop"
        self.move_patterns = []
        self.set_bishop_move_patterns()

    def set_bishop_move_patterns(self):
        i = 1
        while i < 8:
            self.move_patterns.append([i,i])
            self.move_patterns.append([-i,-i])
            self.move_patterns.append([i,-i])
            self.move_patterns.append([-i,i])
            i += 1

    #def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

    #def get_move_patterns(self):
    #    print("checking inheritance")
    #    print(super().get_move_patterns())
    #    return super().get_move_patterns()

    def to_string(self):
        return super().to_string()
    
    def get_color(self):
        return super().get_color()

    def is_valid_move_pattern(self, destination):
        super().is_valid_move_pattern(destination)

