
from turtle import clear
from io import StringIO
import sys
import gameLogic as gl

class integrationTest:
        
    def __init__(self):
        self.possibleDeckVals = set()

    def initDeckVals (self):
        cardNames = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["clubs", "spades", "diamonds", "hearts"]
        for cardName in cardNames:
            for suit in suits:
                self.possibleDeckVals.add(f"{cardName} of {suit}")

    def envSetup(self, input, expected):
        table = gl.BlackjackTable()
        sys.stdin = StringIO()
        sys.stdin.write("q\n")
        sys.stdin.seek(0)
        sys.stdout = StringIO()
        #run the game loop into our buffer
        table.gameLoop()

        testVal = sys.stdout.getvalue()
        expectedVal = self.formatExpected(table, input)
        #do comparisons against testVal
        #clean up
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
        #print(expectedVal)
        print("passed!")
        print(f"{testVal}")


    def addPlayerHitStay(self):
        print("this is todo")

    def formatExpected(self, table: gl.BlackjackTable, input):
        names = input.split("q\n")[0].split("\n")
        #adding names section
        expectedString = "enter q to finish adding player names\n"
        addNameString = "enter a name for a player (gg if your name is q): "
        names[-1] = "q"
        for name in names:
            expectedString += addNameString + name + "\n"
        names = names[:-1]
        #checking for player hits
        for player in table.players:
            expectedString += player.name + " here are your cards\n"
            for card in player.hand:
                expectedString += card.toString() + "\n"
            expectedString += "please enter h for hit or s for stay: "
            expectedString += self.addPlayerHitStay(table, input.split("q\n")[1])

        print("here")
        print(expectedString)


        return expectedString


    def gameLoopTest(self):
        #we first test running gameloop with no players
        table = gl.BlackjackTable()
        table.players = [gl.Player("andrew"), gl.Player("james")]
        table.players[0].hand = [gl.Card(nn = "ace", n = 1, s = "spades"), gl.Card(nn = "queen", n = 10, s = "spades")]
        table.players[1].hand = [gl.Card(nn = "ace", n = 1, s = "diamonds"), gl.Card(nn = "king", n = 10, s = "clubs")]

        self.formatExpected(table, "andrew\njames\nq\n")
        print("done")
        self.envSetup("q\n", "enter q to finish adding player names\nenter a name for a player (gg if your name is q): here are the winners:  []\n")
        #expected result is returning empty array of winners
        #self.testInput("andrew\nq\ns\n")
        #then we run it passing 1 person to the input
        #then we run it with 2 people in the input

        #then we run it with a person hitting 16 times

        #run with  gameL


it = integrationTest()
it.gameLoopTest()