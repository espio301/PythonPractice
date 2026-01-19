from PieceModules.Rook import Rook

class RookTests:
    def run_all(self):
        self.set_rook_move_patterns_test()
        print("finished rook tests")

    def set_rook_move_patterns_test(self):
        actual_patterns = Rook("white", [0,0]).get_move_patterns()
        expected_patterns = self.get_expected_patterns()
        self.check_is_same_length(actual_patterns, expected_patterns)
        for expected in expected_patterns:
            assert expected in actual_patterns
            
    def get_expected_patterns(self):
        expected_patterns = []
        for i in range(-7,8):
            expected_patterns.append([i,0])
            expected_patterns.append([0,1])        
        return expected_patterns

    def check_is_same_length(self, actual, expected):
        assert len(actual) == len(expected)