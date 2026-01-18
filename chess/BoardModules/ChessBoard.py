from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King

LEN_SIDE = 8

class ChessBoard():
    def __init__(self):
        self.board = self.init_board()


    def init_board(self):
        self.board = []
        self.board.append(self.create_initial_king_row("black"))
        self.board.append(self.create_pawn_row("black"))
        for i in range(4):
            self.board.append([0,0,0,0,0,0,0,0])
        self.board.append(self.create_pawn_row("white"))
        self.board.append(self.create_initial_king_row("white"))
        print(self.to_string())

    def is_open_tile(self, coordinates):
        print("here")
        print(coordinates)
        print(coordinates[0])
        return self.board[coordinates[0]][coordinates[1]] == 0

    def to_string(self):
        row_entries = []
        for row in range(LEN_SIDE):
            column_entries = [] 
            for column in range(LEN_SIDE):
                if not self.is_open_tile([row,column]):
                    print("THIS IS WHAT WE HAVE AT THE COORD, ", self.board[row][column] )
                    column_entries.append(self.board[row][column].to_string())
                else:
                    column_entries.append("--")
            row_entries.append(" | ".join(column_entries))
        return "\n".join(row_entries)

    def create_initial_king_row(self, color):
        initialized_row = [Rook(color, [0,0]), Knight(color, [0,0]), Bishop(color, [0,0]), Queen(color, [0,0]), King(color, [0,0]), Bishop(color,[0,0]), Knight(color,[0,0]), Rook(color,[0,0])]
        row = 0
        column = 0
        if color == "white":
            row = LEN_SIDE - 1
        for piece in initialized_row:
            piece.set_coords([row, column])
            column += 1
        return initialized_row
    
    def create_pawn_row(self, color):
        row = 1
        column = 0
        if color == "white":
            row = LEN_SIDE - 2
        initialized_row = []
        for i in range(8):
            initialized_row.append(Pawn(color, [row,column]))
            column += 1
        return initialized_row


ChessBoard().init_board()
    

