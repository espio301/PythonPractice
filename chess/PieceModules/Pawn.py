from Piece import Piece
class Pawn(Piece):
    def __init__(self, color : str, coordinates):
        super().__init__(color, coordinates)

    def get_coords(self):
        return super().get_coords()

    def set_coords(self, coords):
        super().set_coords(coords)

pawn = Pawn("white", [0,0])
pawn.set_coords([1,1])
print(pawn.get_coords())