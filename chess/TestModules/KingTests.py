from PieceModules.King import King
from TestModules.TestHelpers import TestHelpers

class KingTests:

    def __init__(self):
        self.helpers = TestHelpers()

    def run_all(self):
        self.set_king_move_patterns_test()
        print("finished with King unit tests")

    def set_king_move_patterns_test(self):
        expected_patterns = [[1,1], [1,-1], [-1,1], [-1,-1], [1,0], [0,1], [0,-1], [-1,0]]
        actual_patterns = King("white", [0,0]).get_move_patterns()
        self.helpers.assert_equal_elements(expected_patterns, actual_patterns)
        
