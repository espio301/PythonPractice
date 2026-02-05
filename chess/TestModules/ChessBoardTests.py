from BoardModules.ChessBoard import ChessBoard
from PieceModules.Rook import Rook
from PieceModules.Knight import Knight
from PieceModules.Bishop import Bishop
from PieceModules.Queen import Queen
from PieceModules.King import King
from PieceModules.Pawn import Pawn
from TestModules.TestHelpers import TestHelpers
from io import StringIO
from contextlib import redirect_stdout
import sys
#TODO we should be able to run all tests even if one fails, so we need to do try catches appropriately


class ChessBoardTests:
    def run_all(self):
        self.create_initial_board_test()

    def create_initial_board_test(self):
        self.assert_first_last_row_correctness()
        self.assert_pawn_rows_correctness()
        self.assert_empty_rows_are_empty()
        self.is_open_tile_test()
        self.to_string_test()
        self.coord_is_piece_and_is_color_test()
        self.is_valid_movement_test()
        self.is_piece_in_the_way_test()
        self.get_step_direction_test()
        self.move_test()
        self.get_delta_two_points_test()
        self.is_color_in_check_test()
        self.is_color_in_checkmate_test()
        self.is_king_of_color_moveable_test()
        self.get_king_of_color_coords_test()
        self.get_king_potential_moves_test()
        self.get_pieces_for_color_test()
        self.piece_can_take_coord_test()
        self.get_attacked_coords_test()
        self.check_and_execute_win_state_test()
        self.piece_can_uncheck_king_test()
        self.is_valid_castle_movement_test()
        self.is_color_have_valid_moves_test()
        self.get_user_pawn_promo_input_test()
        self.is_stalemate_via_materials_test()
        print("finished with ChessBoard tests")

    def assert_first_last_row_correctness(self):
        chessboard = ChessBoard().board
        row_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            black_piece = chessboard[0][i]
            white_piece = chessboard[7][i]
            assert isinstance(black_piece, row_pieces[i]) and isinstance(white_piece, row_pieces[i]) and black_piece.get_color() == "black" and white_piece.get_color()

    def create_board_white_in_check(self):
        return TestHelpers().create_board_from_pieces([Rook("black", [0,0]),King("white", [7,0]),King("black",[5,5])])

    def create_board_pawn_can_move_diagonally(self):
        return TestHelpers().create_board_from_pieces([King("white",[7,0]), King("black",[0,0]),Pawn("black", [3,1]),Pawn("white",[4,0])])

    def create_pawn_in_way_of_rook(self):
        return TestHelpers().create_board_from_pieces([Pawn("black", [3,1]),Pawn("white",[4,0]),Rook("white",[7,0]), King("white",[7,1]), King("black",[0,7])])

    def create_board_white_in_checkmate(self):
        return TestHelpers().create_board_from_pieces([King("black",[0,0]),Pawn("black", [3,1]),Pawn("white",[4,0]),Pawn("white",[6,0]),Pawn("white",[6,1]),King("white",[7,0]),Rook("black",[7,7])])

    def create_board_white_in_checkmate(self):
        return TestHelpers().create_board_from_pieces([King("black",[0,0]),Pawn("black", [3,1]),Pawn("white",[4,0]),Pawn("white",[6,0]),Pawn("white",[6,1]),King("white",[7,0]),Rook("black",[7,7])])

    def create_rook_to_uncheck_king_board(self):
        return TestHelpers().create_board_from_pieces([King("black",[0,0]),Rook("black", [1,0]),King("white",[7,0]),Rook("white",[6,7])])

    def create_castleable_left_board(self):
        return TestHelpers().create_board_from_pieces([King("black",[0,0]),Rook("black", [1,0]),King("white",[7,4]),Rook("white",[7,0])])

    def create_non_castleable_left_board(self):
        return TestHelpers().create_board_from_pieces([King("black",[0,0]),Rook("black", [1,0]),King("white",[7,4]),Rook("white",[7,0]), Queen("white",[7,1])])
    
    def create_white_in_stalemate_board(self):
        return TestHelpers().create_board_from_pieces([King("white",[7,0]), King("black", [0,0]), Rook("black", [0,1]), Rook("black",[6,7])])

    def create_white_not_stalemate_board(self):
        return TestHelpers().create_board_from_pieces([King("white",[7,0]), King("black", [0,0]), Rook("black", [2,1]), Rook("black",[6,7]), Pawn("white", [6,0])])

    def create_pawn_promo_board(self):
        return TestHelpers().create_board_from_pieces([King("white",[7,0]), King("black", [0,0]), Pawn("white",[1,5])])

    def create_move_into_pawn_promo_board(self):
        return TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Pawn("white", [1,6]), Pawn("black", [6,6]), Knight("white", [7,7])])




    def write_seek_new_stdin(self, write_string):
        sys.stdin = StringIO()
        sys.stdin.write(write_string)
        sys.stdin.seek(0)

    def silent_run(self, func, func_in = None):
        output = StringIO()
        func_output = None
        with redirect_stdout(output):
            if func_in != None:
                func_output = func(func_in)
            else:
                func_output = func()
        return func_output

    def get_stdout_of_func(self, func):
        output = StringIO()
        with redirect_stdout(output):
            func()
        return output.getvalue()

    def assert_pawn_rows_correctness(self):
        chessboard = ChessBoard().board
        for i in range(8):
            black_piece = chessboard[1][i]
            white_piece = chessboard[6][i]
            assert isinstance(black_piece, Pawn) and isinstance(white_piece, Pawn) and black_piece.get_color() == "black" and white_piece.get_color() == "white"

    def assert_empty_rows_are_empty(self):
        chessboard = ChessBoard().board
        for r in range(2,6):
            for c in range(8):
                assert chessboard[r][c] == 0

    def is_open_tile_test(self):
        assert ChessBoard().is_open_tile([0,0]) == False and ChessBoard().is_open_tile([3,3]) == True

    def to_string_test(self): #what's the typical way to do multiline things?
        actual = ChessBoard().to_string()
        expected =   \
"""br | bk | bb | bQ | bK | bb | bk | br  8
bp | bp | bp | bp | bp | bp | bp | bp  7
-- | -- | -- | -- | -- | -- | -- | --  6
-- | -- | -- | -- | -- | -- | -- | --  5
-- | -- | -- | -- | -- | -- | -- | --  4
-- | -- | -- | -- | -- | -- | -- | --  3
wp | wp | wp | wp | wp | wp | wp | wp  2
wr | wk | wb | wQ | wK | wb | wk | wr  1
a    b    c    d    e    f    g    h    """
        assert actual == expected

    def coord_is_piece_and_is_color_test(self):
        empty_coords_give_false =  ChessBoard().coord_is_piece_and_is_color([4,4], "white") == False and ChessBoard().coord_is_piece_and_is_color([4,4], "black") == False
        correct_colored_coords_give_true = ChessBoard().coord_is_piece_and_is_color([0,0], "black") and ChessBoard().coord_is_piece_and_is_color([7,7], "white")
        is_piece_incorrect_color_gives_false = ChessBoard().coord_is_piece_and_is_color([0,0],"white") == False and ChessBoard().coord_is_piece_and_is_color([7,7],"black") == False
        assert empty_coords_give_false and correct_colored_coords_give_true and is_piece_incorrect_color_gives_false

    def is_valid_movement_test(self):
        self.test_valid_movements()
        self.test_invalid_movements()
        self.test_banned_pawn_movement()

    def test_valid_movements(self):
        chessboard = ChessBoard()
        assert chessboard.is_valid_movement([6,0], [5,0]) and chessboard.is_valid_movement([7,1],[5,2])

    def test_invalid_movements(self):
        chessboard = ChessBoard()
        assert chessboard.is_valid_movement([7,0],[6,1]) == False and chessboard.is_valid_movement([7,0],[5,2]) == False
    
    def test_banned_pawn_movement(self):
        self.test_valid_diag_pawn_movement()
        self.test_invalid_diag_pawn_movement()

    def test_valid_diag_pawn_movement(self):
        chessboard = self.create_board_pawn_can_move_diagonally()
        assert chessboard.is_valid_movement([4,0],[3,1])

    def test_invalid_diag_pawn_movement(self):
        assert ChessBoard().is_valid_movement([6,0],[5,1]) == False

    def is_piece_in_the_way_test(self):
        piece_is_in_the_way = ChessBoard().is_piece_in_the_way([7,0],[4,0])
        piece_isnt_in_the_way = ChessBoard().is_piece_in_the_way([6,0], [4,0])
        assert piece_is_in_the_way == True and piece_isnt_in_the_way == False

    def get_step_direction_test(self):
        diagonal_step_works = ChessBoard().get_step_direction([0,0], [1,1]) == [1,1]
        negative_step_works = ChessBoard().get_step_direction([3,3], [2,3]) == [-1,0]
        assert diagonal_step_works and negative_step_works


    def move_test(self):
        chessboard = ChessBoard()
        chessboard.move([6,0],[5,0])
        assert chessboard.board[6][0] == 0 and isinstance(chessboard.board[5][0], Pawn)
    
    def get_delta_two_points_test(self):
        assert ChessBoard().get_delta_two_points([2,1],[3,3]) == [1,2]

    def is_color_in_check_test(self):
        not_in_check_case = ChessBoard().is_color_in_check("white")
        in_check_case = self.create_board_white_in_check().is_color_in_check("white")
        assert not_in_check_case == False and in_check_case == True

    def is_color_in_checkmate_test(self):
        check_but_not_checkmate_result = self.create_board_white_in_check().is_color_in_checkmate("white")
        neither_check_nor_checkmate = ChessBoard().is_color_in_checkmate("white")
        white_in_checkmate = self.create_board_white_in_checkmate().is_color_in_checkmate("white")
        assert neither_check_nor_checkmate == False and check_but_not_checkmate_result == False and white_in_checkmate == True
    
    def is_king_of_color_moveable_test(self):
        when_king_cant_move = ChessBoard().is_king_of_color_moveable("white")
        when_king_checkmated_but_tile_is_open = self.create_board_white_in_checkmate().is_king_of_color_moveable("white")
        when_king_moveable_in_check = self.create_board_white_in_check().is_king_of_color_moveable("white")
        assert when_king_cant_move == False and when_king_checkmated_but_tile_is_open == False and when_king_moveable_in_check == True

    def is_coord_attacked_by_color_test(self):
        if_coord_attacked_by_rook = self.create_board_white_in_checkmate().is_coord_attacked_by_color([7,1])
        if_coord_not_attacked = ChessBoard().is_coord_attacked_by_color([4,4])
        assert if_coord_attacked_by_rook == True and if_coord_not_attacked == False

    def get_king_of_color_coords_test(self):
        chessboard = ChessBoard()
        white_king_coords = chessboard.get_king_of_color_coords("white")
        return white_king_coords == [7,4]

    def get_king_potential_moves_test(self):
        chessboard = ChessBoard()
        potential_moves = chessboard.get_valid_potential_moves(chessboard.board[7][4]) 
        TestHelpers().assert_equal_elements([], potential_moves)
        
    def get_pieces_for_color_test(self):
        self.check_get_white_pieces_given_board_and_amt(ChessBoard(), 16)
        self.check_get_white_pieces_given_board_and_amt(self.create_pawn_in_way_of_rook(),3)
        self.check_get_white_pieces_given_board_and_amt(TestHelpers().create_empty_board(),0)

    def piece_can_take_coord_test(self):
        self.check_piece_cant_take()
        self.check_piece_can_take()
        
    def check_piece_cant_take(self):
        default_board = ChessBoard()
        checkmate_board = self.create_board_white_in_checkmate()
        white_rook = default_board.board[7][0]
        white_pawn = checkmate_board.board[6][1]
        assert default_board.piece_can_take_coord(white_rook, [1,0]) == False and checkmate_board.piece_can_take_coord(white_pawn, [7,7]) == False

    def check_piece_can_take(self):
        pawn_only_board = self.create_board_pawn_can_move_diagonally()
        white_pawn = pawn_only_board.board[4][0]
        assert pawn_only_board.piece_can_take_coord(white_pawn, [3,1])

    def get_attacked_coords_test(self):
        self.check_queen_attack_coords()

    def check_queen_attack_coords(self):
        actual_attacked_coords = ChessBoard().get_attacked_coords(Queen("white", [3,3]))
        expected_attacked_coords = [[4, 4],[2, 2],[4, 2],[2, 4],[5, 5],[1, 1],[5, 1],[1, 5],[6, 6],[0, 0],[6, 0],[0, 6],[7, 7],[3, 0],[0, 3],[3, 1],[1, 3],[3, 2],[2, 3],[3, 3],[3, 3],[3, 4],[4, 3],[3, 5],[5, 3],[3, 6],[6, 3],[3, 7],[7, 3]]
        TestHelpers().assert_equal_elements(actual_attacked_coords, expected_attacked_coords)
        
    def check_and_execute_win_state_test(self):
        chessboard = self.create_board_white_in_checkmate()
        func_output = self.get_stdout_of_func(chessboard.check_and_execute_win_state)
        print("func_out:", func_output)
        assert "0-1" == chessboard.get_winner()

    def check_get_white_pieces_given_board_and_amt(self, chessboard, amount_pieces):
        passed = True
        actual_pieces = chessboard.get_pieces_for_color("white")
        seen_pieces = set()
        for piece in actual_pieces:
            if piece in seen_pieces or piece.get_color() != "white":
                passed = False
            else:
                seen_pieces.add(piece)
        assert passed and len(actual_pieces) == amount_pieces

    def piece_can_uncheck_king_test(self):
        chessboard = self.create_rook_to_uncheck_king_board()
        assert chessboard.piece_can_uncheck_king([6,7])

    def is_valid_castle_movement_test(self):
        self.check_valid_castle_movement()

    def check_valid_castle_movement(self):
        chessboard = self.create_castleable_left_board()
        assert chessboard.is_valid_castle_movement([7,4],[7,0])

    def check_invalid_castle_movement(self):
        chessboard = self.create_non_castleable_left_board()
        assert not chessboard.is_valid_castle_movement([7,4],[7,0])

    def is_color_have_valid_moves_test(self):
        self.check_no_valid_move_stalemate()
        self.check_not_in_stalemate_state()
        self.check_repeated_move_stalemate()

    def check_no_valid_move_stalemate(self):
        chessboard = self.create_white_in_stalemate_board()
        assert chessboard.stalemate_checker()

    def check_not_in_stalemate_state(self):
        chessboard = self.create_white_not_stalemate_board()
        assert not chessboard.stalemate_checker()

    def check_repeated_move_stalemate(self):
        chessboard = ChessBoard()
        board_string = self.create_board_pawn_can_move_diagonally().to_string()
        irrelevant_board_string = self.create_non_castleable_left_board().to_string()
        chessboard.board_states.append(board_string)
        chessboard.board_states.append(board_string)
        chessboard.board_states.append(irrelevant_board_string)
        chessboard.board_states.append(board_string)
        chessboard.board_states.append(board_string)
        chessboard.board_states.append(board_string)
        assert chessboard.stalemate_checker()

    def get_user_pawn_promo_input_test(self):
        self.silent_run(self.pawn_promote_queen)
        self.silent_run(self.move_into_pawn_promo_test)
        self.silent_run(self.black_pawn_promotion_test)
        self.silent_run(self.pawn_attack_to_promotion_test)

    def pawn_promote_queen(self):
        chessboard = self.create_pawn_promo_board()
        self.write_seek_new_stdin("f8=Q\nexit\n")
        chessboard.game_loop()
        assert type(chessboard.board[0][5]) == Queen

    def move_into_pawn_promo_test(self):
        chessboard = self.create_pawn_promo_board()
        self.write_seek_new_stdin("f8=R\nexit\n")
        self.silent_run(chessboard.game_loop)
        assert type(chessboard.board[0][5]) == Rook

    def black_pawn_promotion_test(self):
        chessboard = self.create_pawn_promo_board()
        self.write_seek_new_stdin("f8=N\nexit\n")
        self.silent_run(chessboard.game_loop)
        assert type(chessboard.board[0][5]) == Knight

    def pawn_attack_to_promotion_test(self):
        chessboard = self.create_pawn_promo_board()
        self.write_seek_new_stdin("f8=B\nexit\n")
        self.silent_run(chessboard.game_loop)
        assert type(chessboard.board[0][5]) == Bishop

    def is_stalemate_via_materials_test(self):
        self.check_bishop_king_vs_bishop_king()
        self.check_bishop_king_vs_king()
        self.check_king_vs_king()
        self.check_king_knight_vs_king()
        self.check_king_vs_two_knights()
        self.check_non_stalemate_situations()
    
    def check_bishop_king_vs_bishop_king(self):
        chessboard = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Bishop("white", [2,2]), Bishop("black", [3,3])])
        print(chessboard.to_string())
        assert chessboard.is_stalemate_via_materials()
    
    def check_bishop_king_vs_king(self):
        chessboard = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Bishop("white", [2,2])])
        assert chessboard.is_stalemate_via_materials()

    def check_king_vs_king(self):
        chessboard = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0])])
        assert chessboard.is_stalemate_via_materials()
    
    def check_king_knight_vs_king(self):
        chessboard = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Knight("black", [3,3])])
        assert chessboard.is_stalemate_via_materials()

    def check_king_vs_two_knights(self):
        chessboard = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Knight("black", [3,3]), Knight("black",[4,4])])
        assert chessboard.is_stalemate_via_materials()
    
    def check_non_stalemate_situations(self):
        knight_pawn = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Knight("black", [3,3]), Pawn("black",[4,4])])
        two_knights_pawn = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Knight("black", [3,3]), Knight("black",[4,4]), Pawn("black", [5,5])])
        bishop_vs_bishop = TestHelpers().create_board_from_pieces([King("white", [7,0]), King("black", [0,0]), Knight("black", [3,3]), Bishop("white",[3,3]), Bishop("black", [3,4])])
        assert not knight_pawn.is_stalemate_via_materials() and not two_knights_pawn.is_stalemate_via_materials() and not bishop_vs_bishop.is_stalemate_via_materials()




#TODO make sure cant input bad pawn promo