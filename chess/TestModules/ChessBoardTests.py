from BoardModules.ChessBoard import ChessBoard
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn
from io import StringIO
from contextlib import redirect_stdout
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
        self.get_user_piece_to_move_test()
        self.is_moving_non_king_in_check_test()
        self.is_valid_movement_test()
        print("finished with ChessBoard tests")

    def assert_first_last_row_correctness(self):
        chessboard = ChessBoard().board
        row_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook ]
        for i in range(8):
            black_piece = chessboard[0][i]
            white_piece = chessboard[7][i]
            assert isinstance(black_piece, row_pieces[i]) and isinstance(white_piece, row_pieces[i]) and black_piece.get_color() == "black" and white_piece.get_color()

#TODO eventually I'm going to refactor this into TestHelper. After I make the chess letter/coord converter I'll make a board creator helper with all of these. given string of chess moves it will create a board of that state
    def create_board_white_in_check(self):
        chessboard = ChessBoard()
        chessboard.board = [[Rook("black", [0,0]),0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [King("white", [7,0]),0,0,0,0,0,0,Rook("black",[0,0])]]
        return chessboard

    def create_board_pawn_can_move_diagonally(self):
        chessboard = ChessBoard()
        chessboard.board = [[0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,Pawn("black", [3,1]),0,0,0,0,0,0],\
                            [Pawn("white",[4,0]),0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0]]
        return chessboard

    def write_seek_new_stdin(self, write_string):
        sys.stdin = StringIO()
        sys.stdin.write(write_string)
        sys.stdin.seek(0)

    def silent_run(self, func, func_in = None):
        output = StringIO()
        with redirect_stdout(output):
            if func_in != None:
                func(func_in)
            func()
        return output




#everything above is to be put in a helper class

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

    def get_user_piece_to_move_test(self):
        self.silent_run(self.check_correct_piece_to_move)
        self.silent_run(self.check_user_moves_not_a_piece)
        self.silent_run(self.check_user_moves_other_player_piece)
        self.silent_run(self.check_user_tries_moving_in_check)
        
    def check_correct_piece_to_move(self):
        self.write_seek_new_stdin("0,0\n")
        blacks_move = ChessBoard().get_user_piece_to_move("black")
        self.write_seek_new_stdin("7,7\n")
        white_move = ChessBoard().get_user_piece_to_move("white")
        assert white_move == [7,7] and blacks_move == [0,0]

    def check_user_moves_not_a_piece(self):
        self.write_seek_new_stdin("4,4\n0,0\n")
        incorret_move_first = ChessBoard().get_user_piece_to_move("black")
        assert incorret_move_first == [0,0]

    def check_user_moves_other_player_piece(self):
        self.write_seek_new_stdin("7,7\n0,0\n")
        incorret_move_first = ChessBoard().get_user_piece_to_move("black")
        assert incorret_move_first == [0,0]
    
    def check_user_tries_moving_in_check(self):
        chessboard = self.create_board_white_in_check()
        self.write_seek_new_stdin("7,7\n7,0\n")
        assert chessboard.get_user_piece_to_move("white") == [7,0]

    def is_moving_non_king_in_check_test(self):
        self.silent_run(self.check_user_tries_moving_in_check) #leaving this here for consistency of my testing and in future it may want to be done more thoroughly (feel free to tell me to delete this though, I'm only leaving this comment in case a coach wants to course correct this thought process)

    def is_valid_movement_test(self):
        self.test_valid_movements()
        self.test_invalid_movements()
        self.test_banned_pawn_movement()

    def test_valid_movements(self):
        chessboard = ChessBoard()
        assert chessboard.is_valid_movement([6,0], [5,0]) and chessboard.is_valid_movement([7,1],[5,2])

    def test_invalid_movements(self):
        chessboard = ChessBoard()
        assert chessboard.is_valid_movement([7,0],[6,1]) == False and chessboard.is_valid_movement([7,0],[5,2]) == False
    
    def test_banned_pawn_movement(self):
        self.test_valid_diag_pawn_movement()
        self.test_invalid_diag_pawn_movement()

    def test_valid_diag_pawn_movement(self):
        chessboard = self.create_board_pawn_can_move_diagonally()
        assert chessboard.is_valid_movement([4,0],[3,1])

    def test_invalid_diag_pawn_movement(self):
        assert ChessBoard().is_valid_movement([6,0],[5,1]) == False


