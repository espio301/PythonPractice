import logging
import gameLogic as gl
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



ut = UnitTests()
print(ut.cardInitTest())
print(ut.cardToStringTest())
print(ut.deckInitTest())
