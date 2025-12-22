#a deck has 52 cards
# the dealer deals the four cards, whoever comes closer to 21 wins, if a player goes over 21 they bust and lose
#for simplicity we won't have a special blackjack property just yet as well as no splitting (cause im ngl, I don't actually know how that works in the game xd, lets just add that later :) )

#ok so before thinking about hands and whatnot, lets think about how to store cards. we need to make sure that no two cards dealt are the same.
# if we store them in a list and remove them thats a long operation each time, obviously can keep a seenSet though. that being said if we rng keep getting cards and check if its in the seenSet, then we can technically get unlucky and just keep hitting the same one xd. While unlikely lets think of a new way to do it.
# removing an item from a dictionary is O(1) and so is adding it but how do we obtain a random element from a library.
# 
# ok ai is smarter than me, we can create an array of the cards, then swap whichever one we take with one on the end. We can keep track of how many we have dealt and just random amongs the ones that are valid
#fk it lets give it a shot

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
        self.hi = "hi"


d = Deck().deck
counter = 0
for c in d:
    print(c.__dict__)
    counter += 1
print(counter)