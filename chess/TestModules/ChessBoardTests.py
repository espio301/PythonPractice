from BoardModules.ChessBoard import ChessBoard
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn
from io import StringIO
import sys

class ChessBoardTests:
    def run_all(self):
        self.create_initial_board_test()

    def create_initial_board_test(self):
        self.assert_first_last_row_correctness()
        self.assert_pawn_rows_correctness()
        self.assert_empty_rows_are_empty()
        self.is_open_tile_test()
        self.to_string_test()
        self.coord_is_piece_and_is_color_test()
        self.convert_input_to_coords_test()
        self.get_sanitized_coords_test()
        print("finished with ChessBoard tests")

    def assert_first_last_row_correctness(self):
        chessboard = ChessBoard().board
        row_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook ]
        for i in range(8):
            black_piece = chessboard[0][i]
            white_piece = chessboard[7][i]
            assert isinstance(black_piece, row_pieces[i]) and isinstance(white_piece, row_pieces[i]) and black_piece.get_color() == "black" and white_piece.get_color()

    def assert_pawn_rows_correctness(self):
        chessboard = ChessBoard().board
        for i in range(8):
            black_piece = chessboard[1][i]
            white_piece = chessboard[6][i]
            assert isinstance(black_piece, Pawn) and isinstance(white_piece, Pawn) and black_piece.get_color() == "black" and white_piece.get_color() == "white"

    def assert_empty_rows_are_empty(self):
        chessboard = ChessBoard().board
        for r in range(2,6):
            for c in range(8):
                assert chessboard[r][c] == 0

    def is_open_tile_test(self):
        assert ChessBoard().is_open_tile([0,0]) == False and ChessBoard().is_open_tile([3,3]) == True

    def to_string_test(self): #what's the typical way to do multiline things?
        actual = ChessBoard().to_string()
        expected =   \
"""br | bk | bb | bQ | bK | bb | bk | br
bp | bp | bp | bp | bp | bp | bp | bp
-- | -- | -- | -- | -- | -- | -- | --
-- | -- | -- | -- | -- | -- | -- | --
-- | -- | -- | -- | -- | -- | -- | --
-- | -- | -- | -- | -- | -- | -- | --
wp | wp | wp | wp | wp | wp | wp | wp
wr | wk | wb | wQ | wK | wb | wk | wr"""
        assert actual == expected

    def coord_is_piece_and_is_color_test(self):
        empty_coords_give_false =  ChessBoard().coord_is_piece_and_is_color([4,4], "white") == False and ChessBoard().coord_is_piece_and_is_color([4,4], "black") == False
        correct_colored_coords_give_true = ChessBoard().coord_is_piece_and_is_color([0,0], "black") and ChessBoard().coord_is_piece_and_is_color([7,7], "white")
        is_piece_incorrect_color_gives_false = ChessBoard().coord_is_piece_and_is_color([0,0],"white") == False and ChessBoard().coord_is_piece_and_is_color([7,7],"black") == False
        assert empty_coords_give_false and correct_colored_coords_give_true and is_piece_incorrect_color_gives_false

    def convert_input_to_coords_test(self):
        assert ChessBoard().convert_input_to_coords("6,7") == [6,7]

    def get_sanitized_coords_test(self):
        self.test_correct_coords()
        self.assert_given_coords_not_sanitizable(",")
        self.assert_given_coords_not_sanitizable("j,k")
        self.assert_given_coords_not_sanitizable("00,1")

    def test_correct_coords(self):
        self.write_seek_new_stdin("6,7\n")
        assert ChessBoard().get_sanitized_coords() == [6,7]

    def assert_given_coords_not_sanitizable(self, unsanitizable_string):
        self.write_seek_new_stdin(f"{unsanitizable_string}\n6,7\n")
        assert ChessBoard().get_sanitized_coords() == [6,7]

    def write_seek_new_stdin(self, write_string):
        sys.stdin = StringIO()
        sys.stdin.write(write_string)
        sys.stdin.seek(0)
