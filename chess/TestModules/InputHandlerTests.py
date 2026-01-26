from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn
from BoardModules.ChessBoard import ChessBoard
from InputModules.InputHandler import InputHandler
from TestModules.TestHelpers import TestHelpers
from io import StringIO
from contextlib import redirect_stdout
import sys


class InputHandlerTests():
    def run_all(self):
        self.convert_input_to_coords_test()
        self.get_sanitized_coords_test()
        self.get_user_piece_to_move_test()
        self.is_moving_non_king_in_check_test()
        self.get_user_move_to_coords_test()
        print("finished input handler tests")


    def write_seek_new_stdin(self, write_string):
        sys.stdin = StringIO()
        sys.stdin.write(write_string)
        sys.stdin.seek(0)

    def silent_run(self, func, func_in = None):
        output = StringIO()
        func_output = None
        with redirect_stdout(output):
            if func_in != None:
                func_output = func(func_in)
            else:
                func_output = func()
        return func_output

    def get_stdout_of_func(self, func):
        output = StringIO()
        with redirect_stdout(output):
            func()
        return output.getvalue()

    def create_board_white_in_check(self):
        return TestHelpers().create_board_from_pieces([Rook("black", [0,0]),King("white", [7,0]),King("black",[5,5])])

    def create_pawn_in_way_of_rook(self):
        return TestHelpers().create_board_from_pieces([Pawn("black", [3,1]),Pawn("white",[4,0]),Rook("white",[7,0]), King("white",[7,1]), King("black",[0,7])])



    def convert_input_to_coords_test(self):
        chessboard = ChessBoard()
        assert InputHandler(chessboard).convert_input_to_coords("6,7") == [6,7]

    def get_sanitized_coords_test(self):
        self.test_correct_coords()
        self.test_correct_chess_notation()
        self.silent_run(self.assert_given_coords_not_sanitizable, ",")
        self.silent_run(self.assert_given_coords_not_sanitizable, "j,k")
        self.silent_run(self.assert_given_coords_not_sanitizable, "00,1")

    def test_correct_coords(self):
        self.write_seek_new_stdin("6,7\n")
        chessboard = ChessBoard()
        assert InputHandler(chessboard).get_sanitized_coords() == [6,7]
    
    def test_correct_chess_notation(self):
        self.write_seek_new_stdin("b4\n") #goated opening
        chessboard = ChessBoard()
        assert InputHandler(chessboard).get_sanitized_coords() == [4,1]

    def assert_given_coords_not_sanitizable(self, unsanitizable_string):
        self.write_seek_new_stdin(f"{unsanitizable_string}\n6,7\n")
        chessboard = ChessBoard()
        assert InputHandler(chessboard).get_sanitized_coords() == [6,7]

    def get_user_piece_to_move_test(self):
        self.silent_run(self.check_correct_piece_to_move)
        self.silent_run(self.check_user_moves_not_a_piece)
        self.silent_run(self.check_user_moves_other_player_piece)
        
    def check_correct_piece_to_move(self):
        self.write_seek_new_stdin("0,0\n")
        chessboard = ChessBoard()
        blacks_move = InputHandler(chessboard).get_user_piece_to_move("black")
        self.write_seek_new_stdin("7,7\n")
        white_move = InputHandler(chessboard).get_user_piece_to_move("white")
        assert white_move == [7,7] and blacks_move == [0,0]

    def check_user_moves_not_a_piece(self):
        self.write_seek_new_stdin("4,4\n0,0\n")
        chessboard = ChessBoard()
        incorret_move_first = InputHandler(chessboard).get_user_piece_to_move("black")
        assert incorret_move_first == [0,0]

    def check_user_moves_other_player_piece(self):
        self.write_seek_new_stdin("7,7\n0,0\n")
        chessboard = ChessBoard()
        incorret_move_first = InputHandler(chessboard).get_user_piece_to_move("black")
        assert incorret_move_first == [0,0]
    
    def is_moving_non_king_in_check_test(self):
        self.silent_run(self.check_user_tries_moving_in_check) #leaving this here for consistency of my testing and in future it may want to be done more thoroughly (feel free to tell me to delete this though, I'm only leaving this comment in case a coach wants to course correct this thought process)

    def check_user_tries_moving_in_check(self):
        chessboard = self.create_board_white_in_check()
        self.write_seek_new_stdin("7,7\n7,0\n")
        assert InputHandler(chessboard).get_user_piece_to_move("white") == [7,0]

    def get_user_move_to_coords_test(self):
        self.assert_valid_user_move_to_check()
        self.assert_in_the_way_user_move_to_check()
        self.assert_invalid_user_move_to_check()

    def assert_valid_user_move_to_check(self):
        self.write_seek_new_stdin("5,0\n")
        chessboard = ChessBoard()
        assert self.silent_run(InputHandler(chessboard).get_user_move_to_coords, [6,0]) == [5,0]

    def assert_in_the_way_user_move_to_check(self):
        self.write_seek_new_stdin("0,0\n6,0\n")
        chessboard = self.create_pawn_in_way_of_rook()
        assert self.silent_run(InputHandler(chessboard).get_user_move_to_coords, [7,0]) == [6,0]

    def assert_invalid_user_move_to_check(self):
        self.write_seek_new_stdin("6,1\n6,0\n")
        chessboard = self.create_pawn_in_way_of_rook()
        assert self.silent_run(InputHandler(chessboard).get_user_move_to_coords, [7,0]) == [6,0]
