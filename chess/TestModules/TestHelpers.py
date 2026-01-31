from PieceModules.Piece import Piece
from BoardModules.ChessBoard import ChessBoard
from typing import List
from io import StringIO
from contextlib import redirect_stdout
import sys


class TestHelpers:
    def assert_equal_elements(self, list_one, list_two):
        self.assert_is_same_length(list_one, list_two)
        for el in list_one:
            assert el in list_two

    def assert_is_same_length(self, list_one, list_two):
        assert len(list_one) == len(list_two)

    def create_board_from_pieces(self, pieces: List[Piece]):
        chessboard = self.create_empty_board()
        for piece in pieces:
            row = piece.get_coords()[0]
            col = piece.get_coords()[1]
            chessboard.board[row][col] = piece
        return chessboard

    def create_empty_board(self):
        chessboard = ChessBoard()
        chessboard.board = [[0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
                            [0,0,0,0,0,0,0,0],\
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
        func_output = None
        with redirect_stdout(output):
            if func_in != None:
                func_output = func(func_in)
            else:
                func_output = func()
        return func_output

    def get_stdout_of_func(self, func):
        print("starting get_stdout_of_func")
        output = StringIO()
        with redirect_stdout(output):
            func()
        return output.getvalue()
