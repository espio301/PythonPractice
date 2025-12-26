
from io import StringIO
import sys
import gameLogic as gl

class integrationTest:
        
    def testInput(self, input):
        table = gl.BlackjackTable()
        sys.stdin = StringIO()
        sys.stdin.write(input)
        sys.stdin.seek(0)
        #run the game loop into our buffer
        sys.stdout = StringIO()
        table.gameLoop()
        testVal = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

    def gameLoopTest(self):
        #we first test running gameloop with no players
        sys.stdout
        self.testInput("q\n")
        print("pass")
        #expected result is returning empty array of winners
        self.testInput("andrew\nq\ns\n")
        #then we run it passing 1 person to the input

        #then we run it with 2 people in the input

        #then we run it with a person hitting 16 times

        #run with  gameL

it = integrationTest()
it.gameLoopTest()