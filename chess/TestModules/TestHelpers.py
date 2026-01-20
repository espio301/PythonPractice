from PieceModules.Piece import Piece
from BoardModules.ChessBoard import ChessBoard
from typing import List

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