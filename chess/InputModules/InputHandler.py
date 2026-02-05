from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
CHESS_NOTATION_LETTER_CONVERTER = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
SPECIAL_CODES = {"cancel", "cnotation", "ftnotation", "exit"}
CHESS_NOTATION_TO_TYPE = {"R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}

class InputHandler():
    def __init__(self, chessboard : 'BoardModules.ChessBoard'):
        self.chessboard = chessboard
        self.notation_mode = True
        self.pawn_promo_type = None
        self.force_exit = False

    def get_movement_coords(self, color):
        while not self.force_exit:
            print(self.notation_mode)
            coords = []
            if self.notation_mode:
                coords = self.get_notation_coords(color)
            else:
                coords = self.get_from_to_coords(color)
            print(coords)
            if isinstance(coords[0], str) or isinstance(coords[1],str):
                self.special_code_handler(coords)
                continue
            return coords
        return [-1,-1]

    def special_code_handler(self,codes):
        for code in codes:
            if code == "exit":
                self.force_exit = True
            if code == "cnotation":
                self.notation_mode = True
            if code == "ftnotation":
                self.notation_mode = False

    def is_sanitary_digit(self, digit):
        if not digit.isdigit() or int(digit) < 0 or int(digit) >= LEN_SIDE:
            return False
        return True

    def get_user_input(self, prompt):
        return input(prompt)

    def is_sanitary_coords(self, user_in):
        return len(user_in) == 3 and self.is_sanitary_digit(user_in[0]) and user_in[1] == "," and self.is_sanitary_digit(user_in[2])

    def is_sanitary_notation_tile(self, user_in):
        if len(user_in) == 2:
            letter = user_in[0].lower()
            number = user_in[1]
            return self.letter_and_number_within_bounds(letter, number)
        return False

    def is_sanitary_notation(self, user_in):
        if user_in == "O-O" or user_in == "O-O-O":
            return True
        if '=' in user_in and not self.is_sanitary_promo_notation(user_in):
            return False
        user_in = self.sanitize_extra_notations(user_in.split('=')[0])
        print("is_sanitary_notation:", self.is_sanitary_chars(user_in), self.is_sanitary_format(user_in))
        return self.is_sanitary_chars(user_in) and self.is_sanitary_format(user_in)

    def is_sanitary_chars(self, user_in):
        for c in user_in:
            if c.islower() and not self.is_sanitary_col_or_row(c):
                return False
            if c.isupper() and c not in CHESS_NOTATION_TO_TYPE:
                return False
            if c.isdigit() and not int(c) >= 1 and not int(c) <= LEN_SIDE:
                return False
            return True
        
    def is_sanitary_format(self, user_in):
        if len(user_in) < 2:
            return False
        if not self.is_sanitary_notation_tile(user_in[-2:]):
            return False
        if len(user_in) == 2:
            return self.is_sanitary_notation_tile(user_in)
        if len(user_in) == 3:
            return user_in[0].isalpha()
        if len(user_in) == 4:
            return user_in[0].isupper() and (user_in[1].isdigit() or user_in[1].islower())
        if len(user_in) == 5:
            return self.is_double_disambiguator_format(user_in)
        return False

    def is_double_disambiguator_format(self, user_in):
        if len(user_in) != 5:
            return False
        print("is_double_disambiguator_format:",user_in[0] in CHESS_NOTATION_TO_TYPE, self.is_sanitary_notation_tile(user_in[1]+user_in[2]), self.is_sanitary_notation_tile(user_in[3]+user_in[4]))
        return user_in[0] in CHESS_NOTATION_TO_TYPE and self.is_sanitary_notation_tile(user_in[1]+user_in[2]) and self.is_sanitary_notation_tile(user_in[3]+user_in[4])

    def is_sanitary_col_or_row(self, c):
        if c.isdigit():
            num = int(c)
            return num >= 1 and num <= LEN_SIDE
        if c.isalpha():
            return c >= 'a' and c <= 'h'
        return False

    def letter_and_number_within_bounds(self, letter, number):
        return letter >= 'a' and letter <= 'h' and number.isdigit() and int(number) <= LEN_SIDE and int(number) >= 1

    def get_user_move_to_coords(self, origin):
        print("coords to move to:")
        while True:
            destination = self.get_sanitized_coords()
            if isinstance(destination, str):
                return destination
            if not self.chessboard.is_valid_movement(origin, destination):
                print("input was an invalid movement, please re-enter:")
            else:
                return destination

    def is_valid_piece_to_move(self, color, coords):
        return not self.chessboard.is_color_in_check(color) or isinstance(self.chessboard.board[coords[0]][coords[1]], King) or self.chessboard.piece_can_uncheck_king(coords)

    def get_user_pawn_promo_input(self):
        if self.notation_mode:
            return self.get_notation_promo_piece()
        user_in = input("please input what you'd like to promote the pawn to")
        while not self.pawn_promo_piece(user_in):
            user_in = input("please input what you'd like to promote the pawn to")
        return self.pawn_promo_piece(user_in)

    def get_notation_promo_piece(self):
        promo_piece = self.pawn_promo_type
        self.pawn_promo_type = None
        return promo_piece

    def pawn_promo_piece(self, user_in):
        pawn_promo_piece = {"knight": Knight, "bishop": Bishop, "queen": Queen, "rook": Rook}
        if user_in.lower() not in pawn_promo_piece:
            return None
        return pawn_promo_piece[user_in.lower()]

    def get_notation_coords(self,color):
        while True:
            user_in = self.get_notation_input()
            print("get_notation_coords: ", user_in)
            coords = None
            if user_in in SPECIAL_CODES:
                return [user_in]
            if self.is_sanitary_notation(user_in):
                coords = self.decode_chess_notation(user_in, color)
            print("heres coords -", coords)
            if coords == None or not self.chessboard.is_valid_movement(coords[0], coords[1]):
                print("invalid entry, please re-enter")
                continue
            return coords

    def get_notation_input(self):
        while True:
            user_in = input("input chess notation move: ")
            if user_in in SPECIAL_CODES:
                return user_in
            if len(user_in) < 2:
                continue
            user_in = self.sanitize_extra_notations(user_in)
            return user_in

    def sanitize_extra_notations(self, user_in):
        special_chars = ["x", "+", "#", "?", "!"]
        for c in special_chars:
            user_in = user_in.replace(c, "")
        print("sanitizing extra input: ", user_in)
        return user_in

    def decode_chess_notation(self, user_in, color):
        print("decode_chess_notation user_in:", user_in, self.is_double_disambiguator_format(user_in))
        if self.is_double_disambiguator_format(user_in):
            return self.algebraic_double_disambiguator_converter(user_in)
        if  "O-O" in user_in:
            return self.algebraic_castling_converter(user_in, color)
        if "=" in user_in:
            user_in = self.set_pawn_promo_type(user_in)
        disambiguator = self.get_disambiguator_piece_type(user_in)[0]
        piece_type = self.get_disambiguator_piece_type(user_in)[1]
        return self.algebraic_notation_converter(piece_type, disambiguator, user_in[len(user_in) - 2:], color)

    def get_disambiguator_piece_type(self, user_in):
        piece_type = None
        disambiguator = None
        if len(user_in) == 2:
            return [None,Pawn]
        if user_in[0] not in CHESS_NOTATION_TO_TYPE:
            piece_type = Pawn
            disambiguator = user_in[0]
        else:
            piece_type = CHESS_NOTATION_TO_TYPE[user_in[0]]
        if len(user_in) > 3:
            disambiguator = user_in[1]
        return [disambiguator, piece_type]

    def algebraic_double_disambiguator_converter(self, user_in):
        print("algebraic_double_disambiguator_converter:", user_in)
        start = self.convert_input_to_coords(user_in[1]+user_in[2])
        end = self.convert_input_to_coords(user_in[3]+user_in[4])
        print("algebraic_double_disambiguator_converter:", user_in, start, end)
        return [start,end]

    def set_pawn_promo_type(self, user_in):
        letter = user_in.split('=')[1]
        move = user_in.split('=')[0]
        self.pawn_promo_type = CHESS_NOTATION_TO_TYPE[letter]
        return move

    def is_sanitary_promo_notation(self, user_in):
        print("is_sanitary_promo_notation: ", user_in)
        if "=" not in user_in:
            return False
        promo_input = user_in.split('=')[1]
        move_input = user_in.split('=')[0]
        print("is_sanitary_promo_notation: ", promo_input in CHESS_NOTATION_TO_TYPE, self.is_at_end(move_input), self.is_pawn(move_input))
        return promo_input in CHESS_NOTATION_TO_TYPE and self.is_at_end(move_input) and self.is_pawn(move_input)

    def is_at_end(self, user_in):
        return '1' in user_in or '8' in user_in

    def is_pawn(self, user_in):
        return user_in[0] not in CHESS_NOTATION_TO_TYPE

    def algebraic_castling_converter(self, user_in, color):
        castle_coords = {"O-O-O": [0,0], "O-O": [0,7]}
        king_coord = [0,4]
        castle_coord = castle_coords[user_in]
        if color == "white":
            king_coord[0] = 7
            castle_coord[0] = 7
        print("returning this:", [king_coord,castle_coord])
        return [king_coord,castle_coord]

    def algebraic_notation_converter(self, piece_type, disambiguator, end, color):
        print("algebraic_notation_converter:", piece_type, disambiguator, end, color)
        end_coords = self.convert_input_to_coords(end)
        pieces_of_color = self.chessboard.get_pieces_for_color(color)
        correct_types = self.chessboard.filter_by_type(pieces_of_color, piece_type)
        valid_movement_pieces = self.chessboard.get_pieces_can_move_to_coord(correct_types, end_coords)
        print(correct_types)
        if len(valid_movement_pieces) == 0:
            return None
        print("algebraic_notation_converter valid movement pieces: ", valid_movement_pieces)
        if disambiguator != None:
            disambig_index = self.get_disambiguator_index_int(disambiguator)[0]
            disambig_int = self.get_disambiguator_index_int(disambiguator)[1]
            disambig_piece = self.get_disambiguated_piece(valid_movement_pieces, disambig_index, disambig_int)
            return [disambig_piece.get_coords(), end_coords]
        if len(valid_movement_pieces) > 1:
            exception_str = f"some impossible move happened: {valid_movement_pieces[0].get_coords()}, {valid_movement_pieces[1].get_coords()}, {disambiguator},{end_coords},\n{self.chessboard.to_string()}"
            raise Exception(exception_str)
        print([valid_movement_pieces[0].get_coords(), end_coords])
        return [valid_movement_pieces[0].get_coords(), end_coords]

    def get_disambiguator_index_int(self, disambiguator):
            disambig_is_row = disambiguator.isdigit()
            if disambig_is_row:
                return [0, LEN_SIDE - int(disambiguator)]
            else:
                return [1,CHESS_NOTATION_LETTER_CONVERTER[disambiguator]]

    def get_disambiguated_piece(self, valid_movement_pieces, disambig_index, disambig_int):
        for piece in valid_movement_pieces:
            pce_coords = piece.get_coords()
            print("algebraic_notation_converter disambig index:", disambig_index, "pce coords: ", pce_coords, "disambig_int:", disambig_int, "pce_coords[disambig_index] == disambig_int", pce_coords[disambig_index] == disambig_int)
            if pce_coords[disambig_index] == disambig_int:
                print("get_disambiguated_piece out:", piece, piece.to_string())
                return piece
        return None

    def get_from_to_coords(self,color):
        while self.notation_mode == False:
            move_from = self.get_user_piece_to_move(color)
            if isinstance(move_from,str):
                return [move_from]
            move_to = self.get_user_move_to_coords(move_from)
            return [move_from,move_to]

    def get_user_piece_to_move(self, color):
        print("coords to move from: ")
        while True:
            coords = self.get_sanitized_coords()
            if isinstance(coords,str):
                return coords
            if self.chessboard.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]) or self.chessboard.is_open_tile(coords) or not self.is_valid_piece_to_move(color, coords):
                print("invalid tile, please re-enter: ")
            else:
                return coords

    def get_sanitized_coords(self):
        user_in = input()
        while (not self.is_sanitary_coords(user_in) and not self.is_sanitary_notation_tile(user_in)):
            print(user_in, user_in)
            if user_in in SPECIAL_CODES:
                return user_in
            user_in = input("previous input was invalid notation, please re-enter: ")
        return self.convert_input_to_coords(user_in)

    def convert_input_to_coords(self, user_in):
        if len(user_in) == 2:
            user_in = self.convert_chess_notation_to_standard_input(user_in)
        coords = []
        split_input = user_in.split(",")
        for el in split_input:
            coords.append(int(el))
        return coords

    def convert_chess_notation_to_standard_input(self, user_in):
        letter = user_in[0].lower()
        number = int(user_in[1])
        return f"{LEN_SIDE - number},{CHESS_NOTATION_LETTER_CONVERTER[letter]}"
