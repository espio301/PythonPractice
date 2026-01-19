from TestModules.RookTests import RookTests
from TestModules.QueenTests import QueenTests
from TestModules.PawnTests import PawnTests


def run_unit_tests():
    print("starting")
    rook_test_obj = RookTests()
    queen_test_obj = QueenTests()
    pawn_test_obj = PawnTests()

    rook_test_obj.run_all()
    queen_test_obj.run_all()
    pawn_test_obj.run_all()
    print("finished with unit tests")

run_unit_tests()
