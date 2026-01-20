from PieceModules.Queen import Queen
from PieceModules.Queen import Rook
from PieceModules.Queen import Bishop
from TestModules.TestHelpers import TestHelpers

class QueenTests:

    def __init__(self):
        self.helpers = TestHelpers()

    def run_all(self):
        self.set_queen_move_patterns_test()
        print("finished with queen unit tests")

    def set_queen_move_patterns_test(self):
        actual_patterns = Queen("white",[0,0]).get_move_patterns()
        expected_patterns = self.get_expected_move_patterns()
        self.helpers.assert_equal_elements(actual_patterns, expected_patterns)


    def get_expected_move_patterns(self):
        expected_patterns = []
        rook_patterns = Rook("white", [0,0]).get_move_patterns()
        bishop_patterns = Bishop("white", [0,0]).get_move_patterns()
        for i in rook_patterns:
            expected_patterns.append(i)
        for i in bishop_patterns:
            expected_patterns.append(i)
        return expected_patterns