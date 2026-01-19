from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
#TODO would take too much time right now, but would've been nice to do a get_tile function with [r,c]

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
PIECES_DISREGARD_COLLISIONS = ["knight"]

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

    def is_open_tile(self, coords):
        return self.board[coords[0]][coords[1]] == 0

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
        initialized_row = []
        row = 1
        column = 0
        if color == "white":
            row = LEN_SIDE - 2
        for i in range(8):
            initialized_row.append(Pawn(color, [row,column]))
            column += 1
        return initialized_row

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

    def get_user_input(self, prompt):
        return input(prompt)

    def get_sanitized_coords(self):
        user_in = input()
        while len(user_in) != 3 or not self.is_sanitary_digit(user_in[0]) or user_in[1] != "," or (not self.is_sanitary_digit(user_in[2])):
            user_in = input()
        return self.convert_input_to_coords(user_in)

    def convert_input_to_coords(self, user_in):
        coords = []
        split_input = user_in.split(",")
        for el in split_input:
            coords.append(int(el))
        return coords

    def get_user_piece_to_move(self, color):
        print("coords to move from: ")
        coords = self.get_sanitized_coords()
        while self.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]):
            print("coords to move from: ")
            coords = self.get_sanitized_coords()
        return coords

    def is_valid_movement(self, origin, end):
        origin_piece = self.board[origin[0]][origin[1]]
        origin_color = origin_piece.get_color()
        if self.coord_is_piece_and_is_color(end, origin_color) or not origin_piece.is_valid_move_pattern(end) or self.is_banned_pawn_exception(origin,end):
            return False
        return True


    def is_banned_pawn_exception(self, origin, end): #returns true if is an allowable exception, false otherwise
        delta = self.get_delta_two_points(origin, end)
        piece = self.board[origin[0]][origin[1]]
        if not isinstance(piece, Pawn):
            return False
        if delta in piece.get_exception_patterns() and not self.coord_is_piece_and_is_color(end, OPPOSITE_COLOR[piece.get_color()]):
            return True
        if delta in [[1,0],[-1,0]] and self.board[end[0]][end[1]] != 0:
            return True

        return False


    def is_piece_in_the_way(self, origin, destination):
        direction = self.get_step_direction(origin, destination)
        piece = self.board[origin[0]][origin[1]]
        if piece.get_name() in PIECES_DISREGARD_COLLISIONS:
            return True
        cur_coords = [origin[0] + direction[0], origin[1] + direction[1]]
        while cur_coords != destination:
            if self.board[cur_coords[0]][cur_coords[1]] != 0:
                return True
            cur_coords = [cur_coords[0] + direction[0], cur_coords[1] + direction[1]]
        return False

    def get_step_direction(self, origin, destination):
        step_delta = []
        for i in range(2):
            delta = destination[i] - origin[i]
            if delta == 0:
                step_delta.append(0)
            else:
                step_delta.append(int(delta/abs(delta)))
        return step_delta
        
    def get_user_move_to_coords(self, origin):
        print("coords to move to:")
        destination = self.get_sanitized_coords()
        while not self.is_valid_movement(origin, destination) or self.is_piece_in_the_way(origin, destination):
            print("coords to move to:")
            destination = self.get_sanitized_coords()
        return destination
        print("here")

    def move(self, move_from_coords, move_to_coords):
        piece = self.board[move_from_coords[0]][move_to_coords[1]]
        piece.set_coords(move_to_coords)
        self.board[move_to_coords[0]][move_to_coords[1]] = piece
        self.board[move_from_coords[0]][move_from_coords[1]] = 0

    def get_delta_two_points(self, origin, end):
        delta = []
        for i in range(2):
            coord_delta = end[i] - origin[i]
            delta.append(coord_delta)
        return delta

    def check_detected(self)

    def game_loop(self):
        players = ["white", "black"]
        turn_count = 0
        print("please enter coordinates in the form row,column")
        while not self.game_is_won():
            print(self.to_string())
            color_to_move = players[turn_count%2]
            print(f"{color_to_move} to move")
            move_from_coords = self.get_user_piece_to_move(color_to_move)
            move_to_coords = self.get_user_move_to_coords(move_from_coords)
            self.move(move_from_coords, move_to_coords)
            print("turn_count",turn_count)
            turn_count += 1

board = ChessBoard()
print(board.board[0][0].get_color())
board.game_loop()


