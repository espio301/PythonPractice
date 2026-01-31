from BoardModules.ChessBoard import ChessBoard
import sys
from TestModules.PgnUtils import PgnParser, PgnGame
from TestModules.TestHelpers import TestHelpers
from BoardModules.ChessBoard import ChessBoard
from io import StringIO
from contextlib import redirect_stdout


class IntegrationTests():
    #PgnParser()
    def run_tests(self):
        parser = PgnParser(sys.argv[1])
        parser.parse_file()
        print("integrationtests: ",parser.to_string())
        
        self.test_game(parser.get_games()[0])

    def test_game(self, game : PgnGame):
        chessboard = ChessBoard()
        helpers = TestHelpers()
        move_string = ""
        for move in game.get_moves():
            move_string += f"{move}\n"

        helpers.write_seek_new_stdin(move_string)
        output = StringIO()
        print("starting game loop on this game:", game.to_string())
        try:
            with redirect_stdout(output):
                chessboard.game_loop()
        except:
            print("exception occured in game: ", game.to_string())
        finally:
            print("there was an invalid entry - ", "invalid entry, please re-enter\n" in output.getvalue())

        

tests = IntegrationTests()
tests.run_tests()
