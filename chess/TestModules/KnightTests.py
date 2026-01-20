from PieceModules.Knight import Knight

class KnightTests:
    def run_all(self):
        self.assert_move_pattern_correct()
        print("finished Knight unit tests")
        
        
    def assert_move_pattern_correct(self):
        expected_patterns = Knight("white", [0,0]).get_move_patterns()
        actual_patterns = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
        assert expected_patterns == actual_patterns