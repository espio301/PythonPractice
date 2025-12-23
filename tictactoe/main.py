#game will have a 3x3 array
#game will have 2 players,

#will have a game loop with following steps:
    #player prompted for input
    #sanitize input
    #check win con
    #switch players

class game:
    def __init__(self):
        self.board = [[0 for x in range(3)] for i in range(3)]
        self.curTurn = 0

    def isWon(self, player):
        self.logBoard()
        for row in self.board:
            playerWon = True
            for el in row:
                if el != player:
                    playerWon = False
            if playerWon:
                return True
        for c in range(len(self.board)):
            playerWon = True
            for r in range(len(self.board[0])):
                if self.board[r][c] != player:
                    playerWon = False
            if playerWon:
                return True

        playerWon = True
        for i in range(len(self.board)):
            if self.board[i][i] != player:
                playerWon = False
        if playerWon:
            return True
        playerWon = True
        for i in range(len(self.board[0])):
            print(self.board[i][len(self.board) - i - 1], player)
            if self.board[i][len(self.board) - i - 1] != player:
                playerWon = False
        if playerWon:
            return True

        return False

    def logBoard(self):
        for row in self.board:
            print(row)
            
    def sanitizeSpace(self, input):
        try:
            splitInput = input.split(",")
            r = int(splitInput[0])
            c = int(splitInput[1])
            if self.board[r][c] != 0:
                print("you chose an already chosen spot, please pick again!")
                return False
            return [r,c]
        except IndexError:
            print("out of bounds input")
            return False
        except ValueError:
            print("please input the row and column in the form of r,c where r and c are a integer")
            return False
            
    def gameLoop(self):
        gameOver = False
        while not gameOver:
            activePlayer = 'x'
            if self.curTurn % 2:
                activePlayer = 'o'
            space = self.sanitizeSpace(input(f"{activePlayer}, choose your spot in the form row,column: "))
            while not isinstance(space, list):
                space = self.sanitizeSpace(input("new input: "))
                print(space, isinstance(space,list))
            self.board[space[0]][space[1]] = activePlayer
            print("\n")
            gameOver = self.isWon(activePlayer)
            self.curTurn += 1
        print(f"{activePlayer} won!")

g = game()
print(g.board[:][0])
g.gameLoop()