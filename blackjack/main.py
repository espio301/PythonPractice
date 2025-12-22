#a deck has 52 cards
# the dealer deals the four cards, whoever comes closer to 21 wins, if a player goes over 21 they bust and lose
#for simplicity we won't have a special blackjack property just yet as well as no splitting (cause im ngl, I don't actually know how that works in the game xd, lets just add that later :) )

#ok so before thinking about hands and whatnot, lets think about how to store cards. we need to make sure that no two cards dealt are the same.
# if we store them in a list and remove them thats a long operation each time, obviously can keep a seenSet though. that being said if we rng keep getting cards and check if its in the seenSet, then we can technically get unlucky and just keep hitting the same one xd. While unlikely lets think of a new way to do it.
# removing an item from a dictionary is O(1) and so is adding it but how do we obtain a random element from a library.
# 
# ok ai is smarter than me, we can create an array of the cards, then swap whichever one we take with one on the end. We can keep track of how many we have dealt and just random amongs the ones that are valid
#fk it lets give it a shot
import random


class Card:
    def __init__(self):
        self.numberName = ""
        self.number = 0
        self.suit = ""

#also yes ik I could do this in like one function but this seems better scalability and shouldnt be too much more work if I just get really comfortable definiing classes. I feel like I learn more this way perhaps
class Deck:
    def initializeDeck(self):
        deck = []
        for n in range(1,14):
            for s in ["spade", "clubs", "hearts", "diamonds"]:
                c = Card()
                if n == 1:
                    c.numberName = "ace"
                elif n == 11:
                    c.numberName = "jack"
                elif n == 12:
                    c.numberName = "queen"
                elif n == 13:
                    c.numberName = "king"
                else:
                    c.numberName = str(n)
                c.number = n
                c.suit = s
                deck.append(c)
        return deck

    def __init__(self):
        self.deck = self.initializeDeck()
        self.validCards = 52



class Player:
    def __init__(self, initName = ""):
        self.name = initName
        self.hand = []


class BlackjackTable:
    def __init__(self):
        self.players = []
        self.tableDeck = Deck()

    def getPlayers(self):
        print("enter q to finish adding player names")
        while True:
            userInput = input("enter a name for a player (gg if your name is q): ")
            if userInput == "q":
                break
            self.players.append(Player(userInput))

    def dealCard(self, player: Player):
        cardArr = self.tableDeck.deck
        validCards = self.tableDeck.validCards
        rand = random.randint(0, validCards-1)
        player.hand.append(cardArr[rand])
        temp = cardArr[rand]
        cardArr[rand] = cardArr[validCards - 1]
        cardArr[validCards-1] = temp
        self.tableDeck.validCards -= 1

    def gameLoop(self):
        self.getPlayers()
        #we're going to deal to the players until they have two cards each.
        for player in self.players:
            self.dealCard(player)
            self.dealCard(player)
        for p in self.players:
            print(p.name)
            for c in p.hand:
                print(c.__dict__)
            
        #then we're going to cycle through the players asking if they want to hit, checking their card value after to see if they bust
        #then we check each players hand looking for max hand, keeping track of all the players that won



d = Deck().deck
counter = 0
for c in d:
    print(c.__dict__)
    counter += 1
print(counter)
print("starting gameloop")
table = BlackjackTable()
table.gameLoop()