from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}

class ChessBoard():
    def __init__(self):
        self.board = self.create_initial_board()


    def create_initial_board(self):
        print("initializing")
        board = []
        board.append(self.create_initial_king_row("black"))
        board.append(self.create_pawn_row("black"))
        for i in range(4):
            board.append([0,0,0,0,0,0,0,0])
        board.append(self.create_pawn_row("white"))
        board.append(self.create_initial_king_row("white"))
        return board

    def is_open_tile(self, coordinates):
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

    def coord_is_piece_and_is_color(self, coords, color):
        if self.is_open_tile(coords):
            return False
        return self.board[coords[0]][coords[1]].get_color() == color

    #TODO
    def game_is_won(self):
        return False

    def is_sanitary_digit(self, digit):
        if digit.isdigit() == False or int(digit) < 0 or int(digit) > 7:
            return False
        return True

    def get_sanitized_coords(self):
        user_in = input("coords to move from: ")
        #print(len(user_in))
        #print((not user_in[0].isdigit()))
        #print(user_in[1] != ",")

        while len(user_in) != 3 or not self.is_sanitary_digit(user_in[0]) or user_in[1] != "," or (not self.is_sanitary_digit(user_in[2])):
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
        
        #print("HERE")
        #print(self.board[coords[0]][coords[1]].get_color())
        #print(color)

        while self.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]): #check if the piece is of our color and is a piece
            coords = self.get_sanitized_coords()
        return coords

    def game_loop(self):
        players = ["white", "black"]
        turn_count = 0
        print("please enter coordinates in the form row,column")
        while not self.game_is_won():
            print(self.to_string())
            color_to_move = players[turn_count%2]
            print(f"{color_to_move} to move")
            move_from_coords_ = self.get_user_piece_to_move(color_to_move)
            print("turn_count",turn_count)
            turn_count += 1

board = ChessBoard()
print(board.board[0][0].get_color())
board.game_loop()


