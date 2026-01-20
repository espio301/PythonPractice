from logging import raiseExceptions
from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Piece import Piece
#TODO would take too much time right now, but would've been nice to do a get_tile function with [r,c]
#TODO pawn can transform to whatever Piece if it reaches the end
#TODO I'm not going to worry about stalemate rules at the moment
#checkmate has a lot of rules, I sort of wonder if its deserving to be a different class for readability or if theres something better to help this. maybe a board class and a game_loop/game_mechanics class would've made this more readable
#TODO have to make it impossible to move yourself into check
#TODO Castling
#TODO it should be ok to move another piece than the king if it puts the king out of check
#fastest check mate is 6,5 5,5  1,4 3,4     6,6 4,6     0,3 4,7

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
PIECES_DISREGARD_COLLISIONS = ["knight"]

class ChessBoard():
    def __init__(self):
        self.board = self.create_initial_board()
        self.turn_count = 0
        self.game_is_over = False


    def create_initial_board(self):
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
        while self.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]) or self.board[coords[0]][coords[1]] == 0 or self.is_moving_non_king_in_check(color,coords):
            print("coords to move from: ")
            coords = self.get_sanitized_coords()
        return coords

    def is_moving_non_king_in_check(self, color, coords):
        return self.is_color_in_check(color) and not isinstance(self.board[coords[0]][coords[1]], King)

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

    def move(self, move_from_coords, move_to_coords):
        piece = self.board[move_from_coords[0]][move_from_coords[1]]
        piece.set_coords(move_to_coords)
        self.board[move_to_coords[0]][move_to_coords[1]] = piece
        self.board[move_from_coords[0]][move_from_coords[1]] = 0


    def get_delta_two_points(self, origin, end):
        delta = []
        for i in range(2):
            coord_delta = end[i] - origin[i]
            delta.append(coord_delta)
        return delta

    def is_color_in_checkmate(self, color):
        if self.is_color_in_check(color) and not self.is_king_of_color_moveable(color):
            return True
        #we could probably add stalemate mechanics here if we decide to (should do it but I'm running out of time)
        return False

    def is_king_of_color_moveable(self, color):
        king_coords = self.get_king_of_color_coords(color)
        king = self.board[king_coords[0]][king_coords[1]]
        potential_moves = self.get_potential_moves(king)
        for potential_move in potential_moves:
            if not self.is_coord_attacked_by_color(potential_move, OPPOSITE_COLOR[color]) and not isinstance(self.board[potential_move[0]][potential_move[1]], Piece):
                return True
        return False

    def is_coord_attacked_by_color(self, coord, color):
        enemy_pieces = self.get_pieces_for_color(color)
        for piece in enemy_pieces:
            if self.piece_can_take_coord(piece, coord):
                return True
        return False

    def get_potential_moves(self, piece):
        move_patterns = piece.get_move_patterns()
        potential_moves = []
        illegal_moves = []
        piece_coords = piece.get_coords()
        for pattern in move_patterns:
            potential_moves.append([piece_coords[0] + pattern[0], piece_coords[1] + pattern[1]])
        for potential_move in potential_moves:
            if potential_move[0] < 0 or potential_move[0] >= LEN_SIDE or potential_move[1] < 0 or potential_move[1] >= LEN_SIDE:
                illegal_moves.append(potential_move)
        for illegal_move in illegal_moves:
            potential_moves.remove(illegal_move)
        return potential_moves

    def is_color_in_check(self, color):
        enemy_color = OPPOSITE_COLOR[color]
        other_color_pieces = self.get_pieces_for_color(enemy_color)
        king_coords = self.get_king_of_color_coords(color)
        for piece in other_color_pieces:
            if self.piece_can_take_coord(piece, king_coords):
                return True
        return False

    def get_pieces_for_color(self, color):
        pieces = []
        for r in range(0,LEN_SIDE):
            for c in range(0,LEN_SIDE):
                if self.coord_is_piece_and_is_color([r,c], color):
                    pieces.append(self.board[r][c])
        return pieces

    def piece_can_take_coord(self, piece, coord):
        piece_can_attack_coords = self.get_attacked_coords(piece)
        if not coord in piece_can_attack_coords:
            return False
        if self.is_piece_in_the_way(piece.get_coords(), coord):
            return False
        return True

    def get_king_of_color_coords(self, color):
        for r in range(LEN_SIDE):
            for c in range(LEN_SIDE):
                if self.coord_is_piece_and_is_color([r,c], color) and isinstance(self.board[r][c], King):
                    return [r,c]
        raise Exception("There is no king for this color on the board")

    def get_attacked_coords(self, piece):
        move_patterns = piece.get_move_patterns()
        attacked_coords = []
        piece_coords = piece.get_coords()
        for pattern in move_patterns:
            attacked_coords.append([piece_coords[0]+pattern[0],piece_coords[1]+pattern[1]])
        return attacked_coords

    def check_and_execute_win_state(self):
        if self.is_color_in_checkmate("white"):
            print("black wins!")
            self.game_is_over = True
        if self.is_color_in_checkmate("black"):
            print("white wins!")
            self.game_is_over = True

    def game_loop(self):
        players = ["white", "black"]
        print("please enter coordinates in the form row,column")
        while not self.game_is_over:
            print(self.to_string())
            color_to_move = players[self.turn_count%2]
            print(f"{color_to_move} to move")
            move_from_coords = self.get_user_piece_to_move(color_to_move)
            move_to_coords = self.get_user_move_to_coords(move_from_coords)
            self.move(move_from_coords, move_to_coords)
            print("turn_count",self.turn_count)
            self.check_and_execute_win_state()
            self.turn_count += 1

if __name__ == "__main__":
    board = ChessBoard()
    board.game_loop()