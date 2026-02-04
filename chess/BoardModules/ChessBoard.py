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
        self.winner = ""

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

    def get_winner(self):
        return self.winner

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
                    copy_piece = type_piece(piece.get_color(), piece.get_coords())
                    if (isinstance(piece, Rook) or isinstance(piece, King)) and piece.get_has_moved():
                        copy_piece.set_coords([r,c])
                    if isinstance(piece, Pawn) and piece.get_ranks_moved() > 0:
                        for coords in piece.get_move_history():
                            copy_piece.set_coords(coords)
                    row.append(copy_piece)
                else:
                    row.append(0)
            board.append(row)
        return board

    def create_initial_king_row(self, color):
        row = 0
        if color == "white":
            row = LEN_SIDE - 1
        return [Rook(color, [row,0]), Knight(color, [row,1]), Bishop(color, [row,2]), Queen(color, [row,3]), King(color, [row,4]), Bishop(color,[row,5]), Knight(color,[row,6]), Rook(color,[row,7])]
    
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
            print("piece_can_uncheck king: ", self.is_valid_movement(start_coords, end_coords), self.is_valid_movement(start_coords, end_coords) and self.is_legal_move_via_checked_state(start_coords, end_coords))
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
        board_state_one = self.to_string()
        #print("is_valid_movement - is legal move via checked state : ", self.is_legal_move_via_checked_state(origin, end))
        board_state_two = self.to_string()
        #print("checking diffs", board_state_one == board_state_two, board_state_one, board_state_two)
        if ((not self.coord_is_piece_and_is_color(end, origin_color)) and origin_piece.is_valid_move_pattern(end) and self.is_legal_move_via_checked_state(origin, end)) or self.is_valid_castle_movement(origin,end):
            return True
        return False

    def is_valid_castle_movement(self, origin, end):
        print("checking if valid_castl_movement")
        origin_tile = self.board[origin[0]][origin[1]]
        end_tile = self.board[end[0]][end[1]]

        #print(self.to_string())
        print("checking types and colors")
        print(not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["white", "white"]), not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["black", "black"]))
        if not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["white", "white"]) and not self.is_coords_are_types_and_colors([origin, end], [King,Rook], ["black", "black"]):
            return False
        print("checking has moved")
        print(origin_tile.get_has_moved(), end_tile.get_has_moved())
        if origin_tile.get_has_moved() or end_tile.get_has_moved():
            return False
        print("correct types and neither have moved")
        king_start = origin
        rook_start = end
        king_end = self.get_king_rook_end_post_castle(end)[0]
        rook_end = self.get_king_rook_end_post_castle(end)[1]
        print(not self.is_piece_in_the_way(origin,end), not self.is_color_in_check(origin_tile.get_color()), not self.is_color_in_check_post_movements([[king_start, king_end],[rook_start, rook_end]], origin_tile.get_color()))
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
        if delta in piece.get_attack_patterns() and not self.coord_is_piece_and_is_color(end, OPPOSITE_COLOR[piece.get_color()]):
            return True
        if delta in [[1,0],[-1,0]] and self.board[end[0]][end[1]] != 0:
            return True
        return False

    def is_en_passant(self, origin, end):
        piece = self.board[origin[0]][origin[1]]
        enemy_pawn = self.board[origin[0]][end[1]]
        if isinstance(piece, Pawn) and isinstance(enemy_pawn, Pawn):
            print("checking en passant piece instances:", isinstance(piece, Pawn), isinstance(enemy_pawn,Pawn), piece.is_valid_move_pattern(end), origin, end)
        else:
            print("checking en passant piece instances:", isinstance(piece, Pawn), isinstance(enemy_pawn,Pawn), origin, end)
        if not isinstance(piece, Pawn) or not isinstance(enemy_pawn,Pawn) or not piece.is_valid_move_pattern(end):
            return False
        print("en passanting")
        if len(self.move_history) == 0:
            return False

        prev_move = self.move_history[-1]
        delta_prev_move = self.get_delta_two_points(prev_move[1], prev_move[2])
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
        print("is_color_in_checkmate :", color, self.to_string(),"\n", "color is in check :",self.is_color_in_check(color), "king of color is not moveable:", not self.is_king_of_color_moveable(color), "the threat is not takeable:", not self.is_threat_takeable(color))
        if self.is_color_in_check(color) and not self.is_king_of_color_moveable(color) and not self.is_threat_takeable(color):
            return True
        return False

    def is_threat_takeable(self, color):
        print("is_threat_takeable: ")
        pieces = self.get_pieces_for_color(color)
        threats = self.get_threats_to_king(color)
        print(pieces, threats)
        if len(threats) > 2:
            return False
        if len(threats) == 0:
            return True
        for piece in pieces:
            start = piece.get_coords()
            end = threats[0].get_coords()
            print("is threat takeable, start end is valid movement:", start, end, self.is_valid_movement(start,end))
            if self.piece_can_uncheck_king(start):
                return True

        #check if piece in pieces has valid move to the threat

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
        return len(self.get_threats_to_king(color)) > 0

    def get_threats_to_king(self, color):
        threats = []
        enemy_color = OPPOSITE_COLOR[color]
        other_color_pieces = self.get_pieces_for_color(enemy_color)
        king_coords = self.get_king_of_color_coords(color)
        for piece in other_color_pieces:
            if self.piece_can_take_coord(piece, king_coords):
                threats.append(piece)
        print("get threats to king:")
        for i in threats:
            print(i.get_coords())
        return threats

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
        print("get_king_of_color_coords")
        print(self.to_string())
        print("about to raise exception for no king")
        raise Exception("There is no king for this color on the board")

    def get_attacked_coords(self, piece):
        move_patterns = piece.get_move_patterns()
        if isinstance(piece, Pawn):
            move_patterns = piece.get_attack_patterns()
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
            self.winner = "0-1"
            self.game_is_over = True
        if self.is_color_in_checkmate("black"):
            self.winner = "1-0"
            print("white wins!")
            self.game_is_over = True
        if self.stalemate_checker() and not self.game_is_over:
            print("stalemate")
            self.winner = "1/2-1/2"
            self.game_is_over = True

    def stalemate_checker(self):
        print("stalemate_checker :", self.is_stalemate_via_board_states() )
        return self.is_color_have_valid_moves("white") or self.is_color_have_valid_moves("black") or self.is_stalemate_via_board_states() or self.is_stalemate_via_materials()

    def is_stalemate_via_materials(self):
        white_pcs = self.get_pieces_encoding("white")
        black_pcs = self.get_pieces_encoding("black")
        lack_mats_cases = {(1,0,0,0,0,0), (1,0,1,0,0,0), (1,0,0,1,0,0)}
        pieces_lack_mats = white_pcs in lack_mats_cases and black_pcs in lack_mats_cases
        is_king_vs_two_knights = (white_pcs == (1,0,0,0,0,0) and black_pcs == (1,0,0,2,0,0)) or (black_pcs == (1,0,0,0,0,0) and white_pcs == (1,0,0,2,0,0))

        if white_pcs == (1,0,1,0,0,0) and black_pcs == (1,0,1,0,0,0):
            return self.is_bishop_vs_bishop_stalemate()
        return pieces_lack_mats or is_king_vs_two_knights

    def is_bishop_vs_bishop_stalemate(self):
        white_pieces = self.get_pieces_for_color("white")
        black_pieces = self.get_pieces_for_color("black")
        tile_color = None
        for piece in white_pieces + black_pieces:
            if type(piece) == Bishop:
                if tile_color == None:
                    tile_color = self.get_tile_color(piece.get_coords())
                else:
                    return tile_color == self.get_tile_color(piece.get_coords())

    def get_tile_color(self, coords):
        if (coords[0]+coords[1])%2 == 0:
            return "white"
        return "black"

    def get_pieces_encoding(self, color):
        piece_index = {King:0, Queen:1, Bishop:2, Knight:3, Rook:4, Pawn:5}
        pieces_encoding = [0,0,0,0,0,0]
        for piece in self.get_pieces_for_color(color):
            i = piece_index[type(piece)]
            pieces_encoding[i] += 1
        return tuple(pieces_encoding)

    def is_stalemate_via_board_states(self):
        board_states_map = {}
        for state in self.board_states:
            if state not in board_states_map:
                board_states_map[state] = 0
            board_states_map[state] += 1
            if board_states_map[state] >= 5:
                return True
        print("stalemate_checker:",board_states_map, self.board_states)
        return False

    def movement_handler(self, start, end):
        if self.is_valid_castle_movement(start,end):
            self.castle_movement_handler(start, end)
        else:
            if self.is_en_passant(start,end):
                print("start and end:")
                print(start[0],end[0])
                self.board[start[0]][end[1]] = 0
            self.move(start,end)
        self.pawn_promotion_handler()
        self.board_states.append(self.to_string())

    def is_pawn_to_promote(self, coords, color):
        print("is_pawn_to_promote : ", (color == "white" and coords[0] == 0) or (color == "black" and coords[0] == 7), isinstance(self.board[coords[0]][coords[1]], Pawn))
        print("is_pawn_to_promote : ", (color == "white" and coords[0] == 0) or (color == "black" and coords[0] == 7) and isinstance(self.board[coords[0]][coords[1]], Pawn))

        if ((color == "white" and coords[0] == 0) or (color == "black" and coords[0] == 7)) and isinstance(self.board[coords[0]][coords[1]], Pawn):
            return True
        return False

    def pawn_promotion_handler(self):
        all_pieces = self.get_pieces_for_color("white") + self.get_pieces_for_color("black")
        for piece in all_pieces:
            color = piece.get_color()
            coords = piece.get_coords()
            if self.is_pawn_to_promote(coords, color):
                piece_type = self.input_handler.get_user_pawn_promo_input()
                print("pawn_promotion_handler is pawn to promote: ", self.is_pawn_to_promote(coords, color), piece_type, coords, color,  "\n", self.to_string())

                piece = piece_type(color, [0,0])
                self.board[coords[0]][coords[1]] = piece
                piece.set_coords(coords)
        return piece

    def castle_movement_handler(self,start, end):
        king_end = self.get_king_rook_end_post_castle(end)[0]
        rook_end = self.get_king_rook_end_post_castle(end)[1]
        self.move(start,king_end)
        self.move(end,rook_end)

    def run_movement_handling(self, moving_color):
        from_to_coords = self.input_handler.get_movement_coords(moving_color)
        print("run_movement_handling, from to coords : ", from_to_coords)
        if from_to_coords == [-1,-1]:
            return -1
        print("here's from_to_coords: ", from_to_coords)
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
            if self.run_movement_handling(color_to_move) == -1:
                break
            print("turn_count",self.turn_count)
            self.check_and_execute_win_state()
            self.turn_count += 1


if __name__ == "__main__":
    board = ChessBoard()
    board.game_loop()