from PieceModules.Rook import Rook
from TestModules.TestHelpers import TestHelpers

class RookTests:

    def __init__(self):
        self.helpers = TestHelpers()

    def run_all(self):
        self.set_rook_move_patterns_test()
        print("finished with rook unit tests")

    def set_rook_move_patterns_test(self):
        actual_patterns = Rook("white", [0,0]).get_move_patterns()
        expected_patterns = self.get_expected_patterns()
        self.helpers.assert_is_same_length(actual_patterns, expected_patterns)
        self.helpers.assert_equal_elements(actual_patterns, expected_patterns)


    def get_expected_patterns(self):
        expected_patterns = []
        for i in range(-7,8):
            expected_patterns.append([i,0])
            expected_patterns.append([0,i])        
        return expected_patterns
