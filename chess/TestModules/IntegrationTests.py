import traceback
from BoardModules.ChessBoard import ChessBoard
import sys
from TestModules.PgnUtils import PgnParser, PgnGame
from TestModules.TestHelpers import TestHelpers
from BoardModules.ChessBoard import ChessBoard
from io import StringIO
from contextlib import redirect_stdout
import traceback
ENGINE_OUTPUT_FILE = "chess_engine_out.txt"

class IntegrationTests():

    def run_tests(self):
        open(ENGINE_OUTPUT_FILE, 'w')
        input_file = sys.argv[1]
        frmt = ""
        if len(sys.argv) == 3:
            frmt = sys.argv[2]
        parser = PgnParser(input_file, frmt)
        parser.parse_file()
        print("integrationtests: ",parser.to_string())
        for game in parser.get_games():
            self.test_game(game)

    def test_game(self, game : PgnGame):
        chessboard = ChessBoard()
        helpers = TestHelpers()
        move_string = ""
        print("test_game get moves: ", game.get_moves())
        for move in game.get_moves():
            move_string += f"{move}\n"
        print(f"test_game: adding {move_string} to stdin")
        helpers.write_seek_new_stdin(move_string)
        output = StringIO()
        print("starting game loop on this game:", game.to_string())
        try:
            with redirect_stdout(output):
                chessboard.game_loop()
        except Exception as e:
            print("exception occured in game: ", game.to_string(), e, traceback.format_exc())
        finally:
            with open(ENGINE_OUTPUT_FILE ,'a') as sys.stdout:
                print(output.getvalue())
            sys.stdout = sys.__stdout__
            print("there was an invalid entry - ", "invalid entry, please re-enter\n" in output.getvalue())
            if game.ends_checkmated() or chessboard.get_winner() == "1/2-1/2": 
                print("winners are appropriate: ", chessboard.get_winner() == game.get_result(),"chessboard winner:", chessboard.get_winner(), "game results:", game.get_result())

        

tests = IntegrationTests()
tests.run_tests()
