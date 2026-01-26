import BoardModules
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
    def __init__(self, chessboard : BoardModules):
        self.chessboard = chessboard

    #input
    def is_sanitary_digit(self, digit):
        if not digit.isdigit() or int(digit) < 0 or int(digit) >= LEN_SIDE:
            return False
        return True

    #input
    def get_user_input(self, prompt):
        return input(prompt)

    #input
    def get_sanitized_coords(self):
        user_in = input()
        while not self.is_sanitary_coords(user_in) and not self.is_sanitary_chess_notation(user_in):
            user_in = input("previous input was invalid notation, please re-enter: ")
        return self.convert_input_to_coords(user_in)

    def is_sanitary_coords(self, user_in):
        return len(user_in) == 3 and self.is_sanitary_digit(user_in[0]) and user_in[1] == "," and self.is_sanitary_digit(user_in[2])

    #input
    def is_sanitary_chess_notation(self, user_in):
        if len(user_in) == 2:
            letter = user_in[0].lower()
            number = user_in[1]
            return self.letter_and_number_within_bounds(letter, number)
        return False

    #input 
    def letter_and_number_within_bounds(self, letter, number):
        return letter >= 'a' and letter <= 'h' and number.isdigit() and int(number) <= LEN_SIDE and int(number) >= 1

    #input
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

    #input
    def get_user_piece_to_move(self, color):
        print("coords to move from: ")
        coords = self.get_sanitized_coords()
        while self.chessboard.coord_is_piece_and_is_color(coords, OPPOSITE_COLOR[color]) or self.chessboard.is_open_tile(coords) or not self.is_valid_piece_to_move(color, coords):
            print("invalid tile, please re-enter: ")
            coords = self.get_sanitized_coords()
        return coords

    #input
    def get_user_move_to_coords(self, origin):
        print("coords to move to:")
        destination = self.get_sanitized_coords()
        while not self.chessboard.is_valid_movement(origin, destination):
            print("input was an invalid movement, please re-enter:")
            destination = self.get_sanitized_coords()
        return destination


    #input
    def is_valid_piece_to_move(self, color, coords): #TODO should return True if the piece can block the king from check
        return not self.chessboard.is_color_in_check(color) or isinstance(self.chessboard.board[coords[0]][coords[1]], King) or self.chessboard.piece_can_uncheck_king(coords)

    #input

    #input
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


"""    def algebraic_notation_converter(self, chessboard):
        self.chessboard.get_pieces_for_color()
        user_in = self.get_user_input("algebraic input: ")
        piece = self.decode_input(user_in)["piece"]


    def decode_input(self, user_in):
        pieces = {"R":0, "N":0, "B":0, "Q":0, "K":0}
        len_in = len(user_in)
        end = user_in[len_in-2:len_in]
        piece = user_in[0].upper()
        disambiguator = None
        if piece not in pieces:
            piece = "pawn"
            disambiguator = user_in[0]
        if len_in == 4:
            disambiguator = user_in[1]
        return {"piece": piece, "disambiguator": disambiguator, "end":end}
"""
#InputHandler().algebraic_notation_converter()
