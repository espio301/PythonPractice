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

    def is_open_tile(self, coordinates):
        print(self.to_string())
        return self.board[coordinates[0]][coordinates[1]] == 0

    def to_string(self):
        row_entries = []
        for row in range(LEN_SIDE):
            column_entries = [] 
            for column in range(LEN_SIDE):
                if not self.is_open_tile([row,column]):
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


    def validate_start_point_piece(self):
        pass
    def move_piece(self, start_coord, end_coord):
        
        piece = self.board[start_coord]
    def get_user_action(self):
        piece_origin = input("where is the piece you'd like to move")
        pience_endpoint = input("where do you want to move it to")


    #TODO
    def game_is_won(self):
        return False



    def get_sanitized_coords(self):
        user_in = input("coords to move from: ")
        while len(user_in) != 3 and user_in[0].isdigit() and user_in[1] == "," and user_in[1].isdigit():
            user_in = input("coords to move from: ")
        return self.convert_input_to_coords(user_in)

    def convert_input_to_coords(self, user_in):
        coords = []
        split_input = user_in.split(",")
        for el in split_input:
            coords.append(int(el))
        return coords

    def get_user_piece_to_move(self, color):
        coords = self.get_sanitized_coords()
        print(coords)
        print(self.is_open_tile(coords))
        while not self.is_open_tile(coords) or self.board[coords[0]][coords[1]].get_color() != color: #check if the piece is of our color and is a piece
            coords = self.get_sanitized_coords()
        return coords

    def game_loop(self):
        players = ["white", "black"]
        turn_count = 0
        print("please enter coordinates in the form row,column")
        while not self.game_is_won():
            color_to_move = players[turn_count%2]
            print(f"{color_to_move} to move")
            coords_to_move = self.get_user_piece_to_move(color_to_move)
            print(coords_to_move)
            turn_count += 1

board = ChessBoard()
print(board.to_string())



