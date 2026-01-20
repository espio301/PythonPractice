from PieceModules.Piece import Piece

class PieceTests:
    def run_all(self):
        self.to_string_test()
        self.is_valid_move_pattern_test()
        print("finished with piece tests")

    def to_string_test(self):
        piece = Piece("color", [0,0])
        piece.name = "name"
        assert piece.to_string() == "cn"

    def is_valid_move_pattern_test(self):
        piece = Piece("color", [1,1])
        piece.move_patterns = [[1,1], [2,2]]
        assert piece.is_valid_move_pattern([3,3])