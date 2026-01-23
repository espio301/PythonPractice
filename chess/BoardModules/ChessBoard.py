from logging import raiseExceptions
from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Piece import Piece
from typing import Type
#TODO would take too much time right now, but would've been nice to do a get_tile function with [r,c]
#TODO pawn can transform to whatever Piece if it reaches the end
#TODO I'm not going to worry about stalemate rules at the moment
#checkmate has a lot of rules, I sort of wonder if its deserving to be a different class for readability or if theres something better to help this. maybe a board class and a game_loop/game_mechanics class would've made this more readable
#TODO have to make it impossible to move yourself into check
#TODO Castling
#TODO it should be ok to move another piece than the king if it puts the king out of check
#fastest check mate is 6,5 5,5  1,4 3,4     6,6 4,6     0,3 4,7



#its ok to break abstraction layers a little, if it makes things more approachable/understandable
#long names are a little unreadable as well
#DRY
#also use types xd

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
PIECES_DISREGARD_COLLISIONS = ["knight"]
CHESS_NOTATION_LETTER_CONVERTER = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

class ChessBoard():
    def __init__(self):
        self.board = self.create_initial_board()
        self.turn_count = 0
        self.game_is_over = False
        self.board_states = []


    def create_initial_board(self):
        board = []
        board.append(self.create_initial_king_row("black"))
        board.append(self.create_pawn_row("black"))
        for i in range(4):
            board.append([0,0,0,0,0,0,0,0])
        board.append(self.create_pawn_row("white"))
        board.append(self.create_initial_king_row("white"))
        return board


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

    def is_open_tile(self, coords):
        return self.board[coords[0]][coords[1]] == 0

    def deep_copy_board(self):
        board = []
        for r in range(LEN_SIDE):
            row = []
            for c in range(LEN_SIDE):
                if isinstance(self.board[r][c],Piece):
                    piece = self.board[r][c]
                    type_piece = type(self.board[r][c])
                    row.append(type_piece(piece.get_color(), piece.get_coords()))
                else:
                    row.append(0)
            board.append(row)
        return board

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
        if not digit.isdigit() or int(digit) < 0 or int(digit) >= LEN_SIDE:
            return False
        return True

    def get_user_input(self, prompt):
        return input(prompt)

    def get_sanitized_coords(self):
        user_in = input()
        while not self.is_sanitary_coords(user_in) and not self.is_sanitary_chess_notation(user_in):
            user_in = input()
        return self.convert_input_to_coords(user_in)

    def is_sanitary_coords(self, user_in):
        return len(user_in) == 3 and self.is_sanitary_digit(user_in[0]) and user_in[1] == "," and self.is_sanitary_digit(user_in[2])

    def convert_chess_notation_to_standard_input(self, user_in):
        letter = user_in[0].lower()
        number = int(user_in[1])
        return f"{LEN_SIDE-number},{CHESS_NOTATION_LETTER_CONVERTER[letter]}"

    def is_sanitary_chess_notation(self, user_in):
        if len(user_in) == 2:
            letter = user_in[0].lower()
            number = user_in[1]
            return self.letter_and_number_within_bounds(letter, number)
        return False

    def letter_and_number_within_bounds(self, letter, number):
        return letter >= 'a' and letter <= 'h' and number.isdigit() and int(number) <= LEN_SIDE and int(number) >= 1

    def convert_input_to_coords(self, user_in):
        if len(user_in) == 2:
            user_in = self.convert_chess_notation_to_standard_input(user_in)
        coords = []
        split_input = user_in.split(",")
        for el in split_input:
            coords.append(int(el))
        return coords

    def get_user_piece_to_move(self, color):
        print("coords to move from: ")
        coords = self.get_sanitized_coords()
        while self.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]) or self.is_open_tile(coords) or not self.is_valid_piece_to_move(color, coords):
            print("coords to move from: ")
            coords = self.get_sanitized_coords()
        return coords

    def is_valid_piece_to_move(self, color, coords): #TODO should return True if the piece can block the king from check
        return not self.is_color_in_check(color) or isinstance(self.board[coords[0]][coords[1]], King) or self.piece_can_uncheck_king(coords)

    def piece_can_uncheck_king(self, start_coords):
        piece = self.board[start_coords[0]][start_coords[1]]
        attacked_coords = self.get_attacked_coords(piece)
        for end_coords in attacked_coords:
            if self.is_valid_movement(start_coords, end_coords) and self.is_legal_move_via_checked_state(start_coords, end_coords):
                return True
        return False

    def is_legal_move_via_checked_state(self, start_coords, end_coords):
        piece = self.board[start_coords[0]][start_coords[1]]
        dummy_board = ChessBoard()
        dummy_board.board = self.deep_copy_board()
        dummy_board.move(start_coords, end_coords)
        return not dummy_board.is_color_in_check(piece.get_color())

    def is_color_in_check_post_movements(self, movement_list, color):
        dummy_board = ChessBoard()
        dummy_board.board = self.deep_copy_board()
        for movement in movement_list:
            start_coord = movement[0]
            end_coord = movement[1]
            dummy_board.move(start_coord, end_coord)
        return dummy_board.is_color_in_check(color)


    def is_valid_movement(self, origin, end):
        origin_piece = self.board[origin[0]][origin[1]]
        origin_color = origin_piece.get_color()
        if self.is_coord_is_out_of_bounds(end) or  self.is_banned_pawn_exception(origin,end) or self.is_piece_in_the_way(origin,end):
            return False
        if not self.coord_is_piece_and_is_color(end, origin_color) and origin_piece.is_valid_move_pattern(end) and self.is_legal_move_via_checked_state(origin, end) or self.is_valid_castle_movement(origin,end):
            return True
        return False

    def is_valid_castle_movement(self, origin, end):
        origin_tile = self.board[origin[0]][origin[1]]
        end_tile = self.board[end[0]][end[1]]

        if not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["white", "white"]) and not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["black", "black"]):
            return False
        if origin_tile.get_has_moved() or end_tile.get_has_moved():
            return False
        king_start = origin
        rook_start = end
        king_end = self.get_king_rook_end_post_castle(end)[0]
        rook_end = self.get_king_rook_end_post_castle(end)[1]
        if not self.is_piece_in_the_way(origin,end) and not self.is_color_in_check(origin_tile.get_color()) and not self.is_color_in_check_post_movements([[king_start, king_end],[rook_start, rook_end]], origin_tile.get_color()):
                return True
        return False

    def get_king_rook_end_post_castle(self,rook_position):
            get_king_rook_post_castle_coords = {(7,0): [[7,2],[7,3]], (7,7):[[7,6],[7,5]], (0,0): [[0,2],[0,3]], (0,7):[[0,6],[0,5]]}
            return get_king_rook_post_castle_coords[tuple(rook_position)]

    def is_coords_are_types_and_colors(self, coords, types, colors):
        for i in range(len(coords)):
            coord = coords[i]
            coord_type = types[i]
            color = colors[i]
            if not self.coord_is_piece_and_is_color(coord, color) or not isinstance(self.board[coord[0]][coord[1]], coord_type):
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
            return False

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
        while not self.is_valid_movement(origin, destination):
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
        return False

    def is_color_have_valid_moves(self,color):
        colors_pieces = self.get_pieces_for_color(color)
        for piece in colors_pieces:
            if len(self.get_valid_potential_moves(piece)) > 0:
                return False
        return True

    def is_king_of_color_moveable(self, color):
        king_coords = self.get_king_of_color_coords(color)
        king = self.board[king_coords[0]][king_coords[1]]
        potential_moves = self.get_valid_potential_moves(king)
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

    def get_valid_potential_moves(self, piece):
        potential_moves = self.get_all_potential_moves(piece)
        illegal_moves = []
        for potential_move in potential_moves:
            if not self.is_valid_movement(piece.get_coords(), potential_move):
                illegal_moves.append(potential_move)
        for illegal_move in illegal_moves:
            potential_moves.remove(illegal_move)
        return potential_moves

    def get_all_potential_moves(self, piece):
        potential_moves = []
        piece_coords = piece.get_coords()
        for pattern in piece.get_move_patterns():
            potential_moves.append([piece_coords[0] + pattern[0], piece_coords[1] + pattern[1]])
        
        return potential_moves

    def is_coord_is_out_of_bounds(self, coord):
        return coord[0] < 0 or coord[1] < 0 or coord[0] >= LEN_SIDE or coord[1] >= LEN_SIDE

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
        if coord not in piece_can_attack_coords:
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
            row = piece_coords[0]+pattern[0]
            col = piece_coords[1]+pattern[1]
            if row < 0 or col < 0 or row >= LEN_SIDE or col >= LEN_SIDE:
                continue
            attacked_coords.append([piece_coords[0]+pattern[0],piece_coords[1]+pattern[1]])
        return attacked_coords

    def check_and_execute_win_state(self):
        if self.is_color_in_checkmate("white"):
            print("black wins!")
            self.game_is_over = True
        if self.is_color_in_checkmate("black"):
            print("white wins!")
            self.game_is_over = True
        if self.stalemate_checker() and not self.game_is_over:
            print("stalemate")

    def stalemate_checker(self):
        return self.is_color_have_valid_moves("white") or self.is_color_have_valid_moves("black") or self.is_stalemate_via_board_states()

    def is_stalemate_via_board_states(self):
        board_states_map = {}
        for state in self.board_states:
            if state not in board_states_map:
                board_states_map[state] = 0
            board_states_map[state] += 1
            if board_states_map[state] >= 3:
                return True
        return False

    def movement_handler(self, start, end):
        print("handler",start,end)
        if self.is_valid_castle_movement(start,end):
            self.castle_movement_handler(start,end)
        else:
            print("statement", start,end)
            self.move(start,end)
        self.pawn_promotion_handler()
        self.board_states.append(self.to_string())

    def pawn_promotion_handler(self):
        all_pieces = self.get_pieces_for_color("white") + self.get_pieces_for_color("black")
        for piece in all_pieces:
            color = piece.get_color()
            coords = piece.get_coords()
            if (color == "white" and coords[0] == 0) or (color == "black" and coords[0] == 7):
                piece_type = self.get_user_pawn_promo_input()
                piece = piece_type(color, [0,0])
                self.board[coords[0]][coords[1]] = piece
                piece.set_coords(coords)
        return piece

    def get_user_pawn_promo_input(self):
        user_in = input("please input what you'd like to promote the pawn to")
        while not self.pawn_promo_piece(user_in):
            user_in = input("please input what you'd like to promote the pawn to")
        return self.pawn_promo_piece(user_in)

    def pawn_promo_piece(self, user_in):
        pawn_promo_piece = {"knight":Knight, "Bishop": Bishop, "king": King, "queen": Queen, "rook": Rook}
        if user_in.lower() not in pawn_promo_piece:
            return None
        return pawn_promo_piece[user_in.lower()]

    def castle_movement_handler(self, start,end):
        king_end = self.get_king_rook_post_castle_coords(start,end)[0]
        rook_end = self.get_king_rook_post_castle_coords(start,end)[1]
        self.move(start,king_end)
        self.move(end,rook_end)

    def game_loop(self):
        players = ["white", "black"]
        print("please enter coordinates in the form row,column")
        while not self.game_is_over:
            print(self.to_string())
            color_to_move = players[self.turn_count%2]
            print(f"{color_to_move} to move")
            move_from_coords = self.get_user_piece_to_move(color_to_move)
            move_to_coords = self.get_user_move_to_coords(move_from_coords)
            self.movement_handler(move_from_coords, move_to_coords)
            print("turn_count",self.turn_count)
            self.check_and_execute_win_state()
            self.turn_count += 1

if __name__ == "__main__":
    board = ChessBoard()
    board.game_loop()