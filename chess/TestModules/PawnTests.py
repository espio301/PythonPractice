from PieceModules.Pawn import Pawn

class PawnTests:
    def run_all(self):
        self.move_pattern_test()
        self.assert_moved_pawn_removes_pattern()
        self.get_exception_patterns_test()
        print("finished with pawn unit tests")

    def move_pattern_test(self):
        self.assert_white_move_pattern_correctness()
        self.assert_black_move_pattern_correctness()

    def assert_white_move_pattern_correctness(self):
        unmoved_actual_patterns = Pawn("white", [0,0]).get_move_patterns()
        unmoved_expected_patterns = [[-1,-1], [-1,1], [-1,0], [-2,0]]
        assert unmoved_actual_patterns == unmoved_expected_patterns

    def assert_black_move_pattern_correctness(self):
        unmoved_actual_patterns = Pawn("black", [0,0]).get_move_patterns()
        unmoved_expected_patterns = [[1,1], [1,-1], [1,0], [2,0]]
        assert unmoved_actual_patterns == unmoved_expected_patterns

    def assert_moved_pawn_removes_pattern(self):
        white_pawn = Pawn("white", [0,0])
        white_pawn.set_coords([1,1])
        assert white_pawn.get_move_patterns() == [[-1,-1], [-1,1], [-1,0]]

    def get_exception_patterns_test(self):
        assert Pawn("white", [0,0]).get_attack_patterns() == [[-1,1],[-1,-1]]