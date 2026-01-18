from PieceModules.Pawn import pawn
from PieceModules.Rook import pawn
from PieceModules.Knight import pawn
from PieceModules.Bishop import pawn
from PieceModules.Queen import pawn
from PieceModules.King import pawn

class ChessBoard():
    def __init__(self):
        self.board = self.init_board():


    def init_board(self):
        board = []
        board.append(self.create_initial_king_row("black"))
        board.append(self.create_pawn_row("black"))
        for i in range(4):
            board.append([0,0,0,0,0,0,0,0])
        board.append(self.create_pawn_row("white"))
        board.append(self.create_initial_king_row("white"))
        print(board)

    def self.create_initial_king_row(self, color):
        initialized_row = [Rook(color, [0,0]), Knight(color, [0,0]), Bishop(color, [0,0]), Queen(color, [0,0]), King(color, [0,0]), Bishop(color,[0,0]), Knight(color,[0,0]), Rook(color,[0,0])]
        row = 0
        column = 0
        if color == "white":
            row = 7
        for piece in initialized_row:
            piece.set_coord(row, column):
            column += 1
        return initialized_row
    
    def self.create_pawn_row(self, color):
        row = 1
        column = 0
        if color == "white":
            row = 6
        initialized_row = []
        for i in range(8):
            initialized_row.append(Pawn(color, [row,column]))
            column += 1



    

