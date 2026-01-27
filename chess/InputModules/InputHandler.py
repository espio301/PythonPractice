from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn

LEN_SIDE = 8
OPPOSITE_COLOR = {"white":"black", "black":"white"}
CHESS_NOTATION_LETTER_CONVERTER = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

class InputHandler():
    def __init__(self, chessboard : 'BoardModules.ChessBoard'):
        self.chessboard = chessboard
        user_in = input("enter y to enter chess notation mode, n for regular: ")
        self.notation_mode = user_in == "y"

    def get_movement_coords(self, color):
        if self.notation_mode:
            return self.get_notation_coords(color)
        else:
            return self.get_from_to_coords(color)

    def get_notation_coords(self,color):
        user_in = self.get_sanitary_notation_in()
        return self.algebraic_notation_converter(user_in, color)

    def get_from_to_coords(self,color):
        while True:
            move_from = self.get_user_piece_to_move(color)
            move_to = self.get_user_move_to_coords(move_from)
            if move_to == "x":
                continue
            return [move_from,move_to]

    def is_sanitary_digit(self, digit):
        if not digit.isdigit() or int(digit) < 0 or int(digit) >= LEN_SIDE:
            return False
        return True

    def get_user_input(self, prompt):
        return input(prompt)

    def get_sanitized_coords(self):
        user_in = input()
        while (not self.is_sanitary_coords(user_in) and not self.is_sanitary_notation_tile(user_in)) or user_in == "x":
            if user_in == "x":
                return "x"
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
        coords = self.get_sanitized_coords()
        while coords == "x" or self.chessboard.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]) or self.chessboard.is_open_tile(coords) or not self.is_valid_piece_to_move(color, coords):
            print("invalid tile, please re-enter: ")
            coords = self.get_sanitized_coords()
        return coords

    def get_user_move_to_coords(self, origin):
        print("coords to move to:")
        destination = self.get_sanitized_coords()
        while destination == "x" or not self.chessboard.is_valid_movement(origin, destination):
            if destination == "x":
                return "x"
            print("input was an invalid movement, please re-enter:")
            destination = self.get_sanitized_coords()
        return destination

    def is_valid_piece_to_move(self, color, coords):
        return not self.chessboard.is_color_in_check(color) or isinstance(self.chessboard.board[coords[0]][coords[1]], King) or self.chessboard.piece_can_uncheck_king(coords)

    def get_user_pawn_promo_input(self):
        user_in = input("please input what you'd like to promote the pawn to")
        while not self.pawn_promo_piece(user_in):
            user_in = input("please input what you'd like to promote the pawn to")
        return self.pawn_promo_piece(user_in)

    def pawn_promo_piece(self, user_in):
        pawn_promo_piece = {"knight": Knight, "bishop": Bishop, "queen": Queen, "rook": Rook}
        if user_in.lower() not in pawn_promo_piece:
            return None
        return pawn_promo_piece[user_in.lower()]

    def get_notation_coords(self,color):
        user_in = self.get_notation_input()
        return self.decode_chess_notation(user_in, color)
        

    def get_notation_input(self):
        while True:
            user_in = input("input chess notation move: ")
            if len(user_in) < 2:
                continue
            if 'x' in user_in:
                user_in.replace("x", "")
            return user_in

    def algebraic_notation_handler(self):
        user_in = self.get_notation_input()
        piece = self.decode_chess_notation(user_in)

    def decode_chess_notation(self, user_in, color):
        pieces = {"R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}
        piece = user_in[0].upper()
        disambiguator = None
        if len(user_in) == 2:
            return self.algebraic_notation_converter(Pawn, None, user_in, color)
        if piece not in pieces:
            piece = Pawn
            disambiguator = user_in[0]
        if len(user_in) > 3:
            disambiguator = user_in[1]
        
        return self.algebraic_notation_converter(pieces[piece], disambiguator, user_in[len(user_in) - 2:], color)


    def algebraic_notation_converter(self, piece_type, disambiguator, end, color):
        all_pieces = self.chessboard.get_pieces_for_color(color)
        correct_types = []
        valid_movement_pieces = []
        end_coords = self.convert_input_to_coords(end)
        for piece in all_pieces:
            if isinstance(piece, piece_type):
                correct_types.append(piece)

        for piece in correct_types:
            print(piece.get_coords(),end_coords)
            if self.chessboard.is_valid_movement(piece.get_coords(),end_coords):
                valid_movement_pieces.append(piece)

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
                print(piece_type, disambiguator, end, color)
                print(pce_coords, end_coords)
                return [pce_coords,end_coords]
        print(piece_type, disambiguator, end, color)
        print(pce_coords, end_coords)

        raise Exception("some impossible move happened")

#InputHandler(BoardModules.Chessboard()).algebraic_notation_handler()
