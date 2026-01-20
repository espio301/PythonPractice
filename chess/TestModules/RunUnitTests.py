from TestModules.RookTests import RookTests
from TestModules.QueenTests import QueenTests
from TestModules.PawnTests import PawnTests
from TestModules.PieceTests import PieceTests
from TestModules.KnightTests import KnightTests
from TestModules.KingTests import KingTests
from TestModules.BishopTests import BishopTests
from TestModules.ChessBoardTests import ChessBoardTests


def run_unit_tests():
    print("starting")
    rook_test_obj = RookTests()
    queen_test_obj = QueenTests()
    pawn_test_obj = PawnTests()
    piece_test_obj = PieceTests()
    knight_test_obj = KnightTests()
    king_test_obj = KingTests()
    bishop_test_obj = BishopTests()
    chess_board_tests_obj = ChessBoardTests()

    rook_test_obj.run_all()
    queen_test_obj.run_all()
    pawn_test_obj.run_all()
    piece_test_obj.run_all()
    knight_test_obj.run_all()
    king_test_obj.run_all()
    bishop_test_obj.run_all()
    chess_board_tests_obj.run_all()
    print("finished with unit tests")

run_unit_tests()
