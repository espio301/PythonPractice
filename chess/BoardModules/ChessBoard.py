from logging import raiseExceptions
from PieceModules.Pawn import Pawn
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Piece import Piece
import InputModules.InputHandler as InputModule
from typing import Type

#fastest check mate is 6,5 5,5  1,4 3,4     6,6 4,6     0,3 4,7



#its ok to break abstraction layers a little, if it makes things more approachable/understandable
#long names are a little unreadable as well
#DRY
#also use types xd

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
PIECES_DISREGARD_COLLISIONS = ["knight"]

class ChessBoard():
    def __init__(self):
        self.board = self.create_initial_board()
        self.turn_count = 0
        self.game_is_over = False
        self.board_states = []
        self.move_history = []
        self.input_handler = InputModule.InputHandler(self)


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
        self.add_row_col_indices(row_entries)
        return "\n".join(row_entries)

    def add_row_col_indices(self, row_entries):
        index_to_letter = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
        column_indices = ""
        for i in range(LEN_SIDE):
            row_entries[i] += f"  {LEN_SIDE - i}" 
            column_indices += f"{index_to_letter[i]}    "
        row_entries.append(column_indices)

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
        if self.is_coord_is_out_of_bounds(end) or self.is_banned_pawn_movement(origin,end) or self.is_piece_in_the_way(origin,end):
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

    def is_banned_pawn_movement(self, origin, end):
        delta = self.get_delta_two_points(origin, end)
        piece = self.board[origin[0]][origin[1]]
        if not isinstance(piece, Pawn):
            return False
        if self.is_en_passant(origin,end):
            return False
        if delta in piece.get_exception_patterns() and not self.coord_is_piece_and_is_color(end, OPPOSITE_COLOR[piece.get_color()]):
            return True
        if delta in [[1,0],[-1,0]] and self.board[end[0]][end[1]] != 0:
            return True
        return False

    def is_en_passant(self, origin, end):
        if len(self.move_history) == 0:
            return False
        piece = self.board[origin[0]][origin[1]]
        color = piece.get_color()
        enemy_pawn = self.board[origin[0]][end[1]]
        print(self.move_history)
        prev_move = self.move_history[-1]
        delta_prev_move = self.get_delta_two_points(prev_move[1], prev_move[2])
        #enemy_moved_prev_turn = self.move_history[0] == enemy_pawn
        if piece.get_ranks_moved() == 3 and abs(delta_prev_move[0]) == 2 and prev_move[0] == enemy_pawn:
            print("succeed in en passant")
            return True
        return False
    #e4 a5 e5 d5 d6

    def is_piece_in_the_way(self, origin, destination):
        direction = self.get_step_direction(origin, destination)
        piece = self.board[origin[0]][origin[1]]
        if piece.get_name() in PIECES_DISREGARD_COLLISIONS:
            return False

        cur_coords = [origin[0] + direction[0], origin[1] + direction[1]]
        while cur_coords != destination:
            if  self.is_coord_is_out_of_bounds(cur_coords) or self.board[cur_coords[0]][cur_coords[1]] != 0:
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
        if self.is_valid_castle_movement(start,end):
            self.castle_movement_handler(start,end)
        else:
            self.move(start,end)
            if self.is_en_passant:
                print("start and end:")
                print(start[0],end[0])
                self.board[start[0]][end[1]] = 0
        self.pawn_promotion_handler()
        self.board_states.append(self.to_string())

    def pawn_promotion_handler(self):
        all_pieces = self.get_pieces_for_color("white") + self.get_pieces_for_color("black")
        for piece in all_pieces:
            color = piece.get_color()
            coords = piece.get_coords()
            if (color == "white" and coords[0] == 0) or (color == "black" and coords[0] == 7):
                piece_type = self.input_handler.get_user_pawn_promo_input()
                piece = piece_type(color, [0,0])
                self.board[coords[0]][coords[1]] = piece
                piece.set_coords(coords)
        return piece

    def castle_movement_handler(self, start,end):
        king_end = self.get_king_rook_post_castle_coords(start,end)[0]
        rook_end = self.get_king_rook_post_castle_coords(start,end)[1]
        self.move(start,king_end)
        self.move(end,rook_end)

    def run_movement_handling(self, moving_color):
        from_to_coords = self.input_handler.get_movement_coords(moving_color)
        self.movement_handler(from_to_coords[0], from_to_coords[1])
        self.add_move_history(from_to_coords)

    def add_move_history(self, from_to_coords):
        start = from_to_coords[0]
        end = from_to_coords[1]
        piece = self.board[end[0]][end[1]]
        self.move_history.append([piece,start,end])

    def game_loop(self):
        players = ["white", "black"]
        print("please enter coordinates in the form row,column, enter x to restart your input")
        while not self.game_is_over:
            print(self.to_string())
            color_to_move = players[self.turn_count%2]
            print(f"{color_to_move} to move")
            self.run_movement_handling(color_to_move)
            print("turn_count",self.turn_count)
            self.check_and_execute_win_state()
            self.turn_count += 1

if __name__ == "__main__":
    board = ChessBoard()
    board.game_loop()