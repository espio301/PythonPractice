import logging
import gameLogic as gl
import sys
from io import StringIO

#deck = gl.Deck()
#card = gl.Card()

#print(deck.toString())

#we should have thorough testing for each function
class UnitTests:

    def cardInitTest(self):
        try:
            card = gl.Card()
            if card.suit == "" and card.number == 0 and card.numberName == "":
                return True
            raise Exception
        except Exception as error:
            return False

    def cardToStringTest(self):
        try:
            card = gl.Card()
            if card.toString() == "" + str(card.numberName) + " of " + str(card.suit):
                return True
            raise Exception
        except Exception as error:
            return False

    #this unit test uses toString, which we probably shouldnt and we can just make a different way to string a card here
    def deckInitTest(self):
        try:
            deck = gl.Deck()
            if deck.validCards != 52 and len(deck.deck) != 52:
                return False
            cardSet = set()
            #we can actually prove we have 1 of each card without hard coding anything by defining that each card is unique, and then that there are 13 of each suit and 4 of each card! pretty neat if you ask me :)
            for card in deck.deck:
                if card.toString() not in cardSet:
                    cardSet.add(card.toString())
                else:
                    return False
            if len(cardSet) != 52:
                return False
            #check suits are correct
            suitMap = {"spades": 0, "clubs": 0, "hearts": 0 , "diamonds": 0}
            for card in deck.deck:
                if card.suit not in suitMap:
                    return False
                suitMap[card.suit] += 1
            for k in suitMap:
                if suitMap[k] != 13:
                    return False
            print(suitMap)

            #checking number Names
            numberNameMap = {"ace": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "jack": 0, "queen": 0, "king": 0}
            for card in deck.deck:
                nn = card.numberName
                if nn not in numberNameMap:
                    numberNameMap[nn] = 0
                numberNameMap[nn] += 1
            print(numberNameMap)
            for k in numberNameMap:
                if numberNameMap[k] != 4:
                    return False

            numberMap = {"ace" : [1,0], "2" : [2,0], "3" : [3,0], "4": [4,0], "5": [5,0], "6": [6,0], "7": [7,0], "8": [8,0], "9": [9,0], "10": [10,0], "jack": [10,0], "queen": [10,0], "king": [10,0]}
            for card in deck.deck:
                if card.numberName in numberMap and numberMap[card.numberName][0] == card.number:
                     numberMap[card.numberName][1] += 1
            print(numberMap)
            for k in numberMap:
                if numberMap[k][1] != 4:
                    return False
            return True
        except Exception as e:
            print("failed")
            return False

    def deckToStringTest(self):
        try:
            deck = gl.Deck()
            validCards = deck.toString().split("\n")[0]
            validList = validCards.split(":")
            if validList[0] != "valid cards" and int(validList[1]) != 52:
                return False
            cardList = deck.toString().split("\n")[1].split(", ")
            cardName = {"ace", "2", "3" , "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"}
            suitName = {"spades", "clubs", "hearts", "diamonds"}
           
            for card in cardList:
                cardSplit = card.split(" of ")
                if cardSplit[0] not in cardName or cardSplit[1] not in suitName:
                    print(f"failed:{cardSplit[0]} , {cardSplit[0] not in cardName} \n{cardSplit[1]} , {cardSplit[1] not in suitName}" )
                    return False
            return True
        except Exception as e:
            print("failed: ", e)
            return False

    #need to implement if there are no players
    def getPlayersTest(self):
        try:
            sys.stdin = StringIO()
            table = gl.BlackjackTable()
            passed = True
            #standard test
            sys.stdin.write("andrew\njames\nq\n")
            sys.stdin.seek(0)
            table.getPlayers()
            for player in table.players:
                print(player.toString())
            if table.players[0].name != "andrew" and table.players[1].name != "james":
                print("failed standard test")
                passed = False
            table = gl.BlackjackTable()
            sys.stdin.write("q\n")
            sys.stdin.seek(15)
            table.getPlayers()
            if len(table.players) != 0:
                print("failed empty player list")
                passed = False
            #nonstring input, technically speaking this should still pass as technically people can have numbers in their name (elons kid has non english alphabet symbols at least)
            table = gl.BlackjackTable()
            sys.stdin.write("123\nq\n")
            sys.stdin.seek(17)
            table.getPlayers()
            if len(table.players) != 1 and table.players[0] != "123":
                print("failed empty player list")
                passed = False
            return passed
        except Exception as e:
            print(f"failed with error: {e}")
            return False
        
        #mainly need to assure aces logic works appropriately
    def calculateHandTest(self):
    #check standard test
        passed = True
        c1 = gl.Card("2",2,"clubs")
        c2 = gl.Card("3",3,"clubs")
        p1 = gl.Player("andrew", [c1,c2])
        if p1.calculateHand() != 5:
            print(f"failed standard test, hand val was {p1.calculateHand()} when cards were {c1.numberName} and {c2.numberName}")
            passed = False

        c1 = gl.Card("ace",1,"clubs")
        c2 = gl.Card("ace",1,"spade")
        p1 = gl.Player("andrew", [c1,c2])
        if p1.calculateHand() != 12:
            print(f"failed double aces test, hand val was {p1.calculateHand()} when cards were {c1.numberName} and {c2.numberName}")
            passed = False

        c1 = gl.Card("jack",10,"clubs")
        c2 = gl.Card("ace",1,"spade")
        c3 = gl.Card("5",5,"spade")

        p1 = gl.Player("andrew", [c1,c2,c3])
        if p1.calculateHand() != 16:
            print(f"failed 3 cards with ace thats less than 11 test, hand val was {p1.calculateHand()} when cards were {c1.numberName}, {c2.numberName}, and {c3.numberName}")
            passed = False

        c1 = gl.Card("jack",10,"clubs")
        c2 = gl.Card("9",9,"spade")
        c3 = gl.Card("10",10,"spade")
        p1 = gl.Player("andrew", [c1,c2,c3])
        if p1.calculateHand() != 29:
            print(f"bust test, hand val was {p1.calculateHand()} when cards were {c1.numberName}, {c2.numberName}, and {c3.numberName}")
            passed = False

        c1 = gl.Card("ace",1,"clubs")
        c2 = gl.Card("ace",1,"spade")
        c3 = gl.Card("10",10,"spade")
        p1 = gl.Player("andrew", [c1,c2,c3])
        if p1.calculateHand() != 12:
            print(f"failed multiple aces, neither 11 test, hand val was {p1.calculateHand()} when cards were {c1.numberName}, {c2.numberName}, and {c3.numberName}")
            passed = False
        return passed
        #can assume there exists players as we test for this beforehand
    def getWinnersTest(self):
        try:
            #standard test 
            table = gl.BlackjackTable()
            passed = True
            c11 = gl.Card("9", 9, "spades")
            c12 = gl.Card("ace", 1, "clubs")
            c21 = gl.Card("8", 8, "spades")
            c22 = gl.Card("10", 10, "spades")
            p1 = gl.Player("andrew", [c11,c12])
            p2 = gl.Player("james", [c21,c22])
            if table.getWinners([p1,p2]) != ["andrew"]:
                print(f"failed standard test between {p1.hand.toString()} and {p2.hand.toString()}")
                passed = False

            #test tie
            c11 = gl.Card("9", 9, "spades")
            c12 = gl.Card("ace", 1, "clubs")
            c21 = gl.Card("8",10, "diamonds")
            c22 = gl.Card("10", 10, "spades")
            p1 = gl.Player("andrew", [c11,c12])
            p2 = gl.Player("james", [c21,c22])
            if table.getWinners([p1,p2]) != ["andrew", "james"]:
                print(f"failed tie between {p1.hand.toString()} and {p2.hand.toString()}")
                passed = False

            #test for a tie then a winner after
            c31 = gl.Card("10",10,"spade")
            c32 = gl.Card("ace", 1, "clubs")
            p3 = gl.Player("shomik", [c31, c32])
            if table.getWinners([p1,p2,p3]) != ["shomik"]:
                print(f"failed tie at first, then a winner is apparent: {p1.hand.toString()}, {p2.hand.toString()}, then {p3.hand.toString()}")
                passed = False 

            #test empty
            if table.getWinners([]) != []:
                print("failed empty player list")
                passed = False
            return passed
        except Exception as e:
            print(f"failed with error: {e}")
            return False
        #test for one player who bust
        #standard test between two players
        #standard test between 3 players

ut = UnitTests()
deck = gl.Deck()
#sys.stdin.write("myinput")
#sys.stdin.seek(0)  # rewind, so input() can read
#text = input()
#print(f"{text=}")

print(ut.getWinnersTest())
"""print(ut.cardInitTest())
print(ut.cardToStringTest())
#print(ut.deckInitTest())
print(ut.deckToStringTest())
"""