from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn

#how better should I have gone about special code handling

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
CHESS_NOTATION_LETTER_CONVERTER = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
SPECIAL_CODES = {"cancel", "cnotation", "ftnotation"}
CHESS_NOTATION_TO_TYPE = {"R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}
class InputHandler():
    def __init__(self, chessboard : 'BoardModules.ChessBoard'):
        self.chessboard = chessboard
        self.notation_mode = True
        self.pawn_promo_type = None

    def get_movement_coords(self, color):
        while True:
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

    def get_from_to_coords(self,color):
        while self.notation_mode == False:
            move_from = self.get_user_piece_to_move(color)
            if isinstance(move_from,str):
                return [move_from]
            move_to = self.get_user_move_to_coords(move_from)
            return [move_from,move_to]

    def special_code_handler(self,codes):
        for code in codes:
            if code == "cancel":
                return
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

    def get_sanitized_coords(self):
        user_in = input()
        while (not self.is_sanitary_coords(user_in) and not self.is_sanitary_notation_tile(user_in)) or user_in == "x":
            print(user_in, user_in)
            if user_in in SPECIAL_CODES:
                return user_in
            user_in = input("previous input was invalid notation, please re-enter: ")
        return self.convert_input_to_coords(user_in)

    def is_sanitary_coords(self, user_in):
        return len(user_in) == 3 and self.is_sanitary_digit(user_in[0]) and user_in[1] == "," and self.is_sanitary_digit(user_in[2])

    def is_sanitary_notation_tile(self, user_in):
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

    def convert_chess_notation_to_standard_input(self, user_in):
        letter = user_in[0].lower()
        number = int(user_in[1])
        return f"{LEN_SIDE - number},{CHESS_NOTATION_LETTER_CONVERTER[letter]}"

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
            if user_in in SPECIAL_CODES:
                return [user_in]
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
            if 'x' in user_in:
                user_in.replace("x", "")
            return user_in

    def decode_chess_notation(self, user_in, color):
        if user_in == "0-0" or user_in == "0-0-0":
            return self.algebraic_castling_converter(user_in, color)
        print("decode_chess_notation statement: ","=" in user_in, (self.is_pawn(user_in) and self.is_at_end(user_in)))
        if "=" in user_in or (self.is_pawn(user_in) and self.is_at_end(user_in)):
            if not self.is_sanitary_promo_notation(user_in):
                return None
            user_in = self.set_pawn_promo_type(user_in)
            print("decode_chess_notation 1:", self.pawn_promo_type)
        pieces = {"R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}
        piece = user_in[0].upper()
        piece_type = None
        disambiguator = None
        if len(user_in) == 2:
            return self.algebraic_notation_converter(Pawn, None, user_in, color)
        if piece not in pieces:
            piece_type = Pawn
            disambiguator = user_in[0]
        else:
            piece_type = pieces[piece]
        if len(user_in) > 3:
            disambiguator = user_in[1]
        return self.algebraic_notation_converter(piece_type, disambiguator, user_in[len(user_in) - 2:], color)

    def set_pawn_promo_type(self, user_in):
        pieces = {"R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}
        letter = user_in.split('=')[1]
        move = user_in.split('=')[0]
        self.pawn_promo_type = pieces[letter]
        return move

    def is_sanitary_promo_notation(self, user_in):
        print("is_sanitary_promo_notation: ", user_in)
        promo_input = user_in.split('=')[1]
        move_input = user_in.split('=')[0]
        print("is_sanitary_promo_notation: ", promo_input in CHESS_NOTATION_TO_TYPE, self.is_at_end(move_input), self.is_pawn(move_input))
        return promo_input in CHESS_NOTATION_TO_TYPE and self.is_at_end(move_input) and self.is_pawn(move_input)

    def is_at_end(self, user_in):
        return '1' in user_in or '8' in user_in

    def is_pawn(self, user_in):
        return user_in[0].upper() not in CHESS_NOTATION_TO_TYPE

    def algebraic_castling_converter(self, user_in, color):
        castle_coords = {"0-0-0": [0,0], "0-0": [0,7]}
        king_coord = [0,4]
        castle_coord = castle_coords[user_in]
        if color == "white":
            king_coord[0] = 7
            castle_coord[0] = 7
        print("returning this:", [king_coord,castle_coord])
        return [king_coord,castle_coord]

    def algebraic_notation_converter(self, piece_type, disambiguator, end, color):
        print("algebraic_notation_converter:", piece_type, disambiguator, end, color)
        all_pieces = self.chessboard.get_pieces_for_color(color)
        correct_types = []
        valid_movement_pieces = []
        end_coords = self.convert_input_to_coords(end)
        for piece in all_pieces:
            if isinstance(piece, piece_type):
                correct_types.append(piece)
        print(all_pieces)
        print(correct_types)
        for piece in correct_types:
            print("here")
            print(piece.get_coords(),end_coords)
            if self.chessboard.is_valid_movement(piece.get_coords(),end_coords):
                valid_movement_pieces.append(piece)
        if len(valid_movement_pieces) == 0:
            return None
        print(valid_movement_pieces)
        if disambiguator != None:
            disambig_int = 0
            disambig_is_row = disambiguator.isdigit()
            disambig_index = 1
            if disambig_is_row:
                disambig_index = 0
            if disambiguator.isdigit():
                disambig_int = int(disambiguator)
            else:
                disambig_int = CHESS_NOTATION_LETTER_CONVERTER[disambiguator]

            for piece in valid_movement_pieces:
                pce_coords = piece.get_coords()
                if pce_coords[disambig_index] == disambig_int:
                    print("checking notation converter")
                    print(piece_type, disambiguator, end, color)
                    print(pce_coords, end_coords)
                    return [pce_coords,end_coords]
            print("algebraic_notation_converter - vars")
            print(piece_type, disambiguator, end, color)
        print("algebraic_notation_converter - vars2" )
        print(piece_type, disambiguator, end, color)
        if len(valid_movement_pieces) > 1 and disambiguator == None:
            raise Exception("some impossible move happened")
        print([valid_movement_pieces[0].get_coords(), end_coords])
        return [valid_movement_pieces[0].get_coords(), end_coords]

