from PieceModules.Bishop import Bishop
from TestModules.TestHelpers import TestHelpers

class BishopTests:

    def __init__(self):
        self.helpers = TestHelpers()

    def run_all(self):
        self.set_bishop_move_patterns_test()
        print("finished with Bishop unit tests")

    def set_bishop_move_patterns_test(self):
        expected_patterns = self.get_expected_bishop_patterns()
        actual_patterns = Bishop("white", [0,0]).get_move_patterns()
        self.helpers.assert_equal_elements(expected_patterns, actual_patterns)

    def get_expected_bishop_patterns(self):
        expected_patterns = []
        for i in range(1,8):
            expected_patterns.append([i,i])
            expected_patterns.append([-i,-i])
            expected_patterns.append([-i,i])
            expected_patterns.append([i,-i])
        return expected_patterns