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



#TODO implement dealer
#add custom to string function for different classes,
#dont use magic methods

SUITS_LIST = ["spades", "clubs", "hearts", "diamonds"]
RANKS_LIST = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
VALID_ACTIONS = {"s", "h"}
class Card:
    def __init__(self, rank : str, value : int, suit : str):
        self.rank = rank
        self.value = value
        self.suit = suit
        
    def to_string(self):
        return "" + str(self.rank) + " of " + str(self.suit)

    def is_ace(self):
        return self.rank == "ace"

#also yes ik I could do this in like one function but this seems better scalability and shouldnt be too much more work if I just get really comfortable definiing classes. I feel like I learn more this way perhaps
class Deck:
    def __init__(self):
        self.deck = self.initialize_deck()

    def initialize_deck(self):
        deck = []
        #theres perhaps a better way to write this array but is fine for readability?
        for i, init_rank in enumerate(RANKS_LIST):
            for init_suit in SUITS_LIST:
                init_value = i + 1
                if init_value >= 10:
                    init_value = 10
                deck.append(Card(init_rank, init_value, init_suit ))
        return deck

    def to_string(self):
        deck_string = f"cards in deck: {str(len(self.deck))}\n"
        for c in self.deck:
            deck_string += ", ".join([deck_string, c.to_string()])
        return deck_string



class Player:
    def __init__(self, name : str, cards = []):
        self.name = name
        self.hand = []
        for card in cards:
            self.hand.append(card)
    
    def didBust(self):
        if self.calculate_hand() > 21:
            return True
        return False

    def calculate_hand(self):
        total = 0
        aces_count = 0
        for card in self.hand:
            if not card.is_ace():
                total += card.value
            else:
                aces_count += 1
        #we would only ever want 1 ace to count as an 11. if we have an ace, and we don't bust for one to count as an 11, then our total is our expected sum, but one ace is an 11.
        if total + 11 + aces_count - 1  <= 21 and aces_count >= 1:
            total += 11 + aces_count - 1
        #otherwise, we don't want the ace to count as 11, and so each ace would count as 1
        else:
            total += aces_count
        return total

    def to_string(self):
        player_string = f"{self.name}, hand is: "
        if len(self.hand) == 0:
            return player_string + "empty"

        card_list = []
        for card in self.hand:
            card_list.append(card.to_string())
        return  player_string + ", ".join(card_list)

class BlackjackTable:
    def __init__(self):
        self.players = []
        self.table_deck = Deck()
        self.used_cards = Deck()

    def player_hit(self, player: Player):
        self.dealCard(player)
        return player.calculate_hand()

    def player_stay(self, player: Player):
        return player.calculate_hand()

    def add_player(self, player: Player):
        self.players.append(player)

    def get_players(self):
        print("enter q to finish adding player names")
        while True:
            userInput = input("enter a name for a player (gg if your name is q): ")
            if userInput == "q":
                break
            #print(f"adding user with the name {userInput}")
            self.add_player(Player(userInput))
        return

    # the book mentions output arguments are bad, is this fine or should this be changed?
    def deal_card(self, player: Player):
        card_to_deal = self.table_deck.deck.pop()
        player.hand.append(card_to_deal)
        self.used_cards.append(card_to_deal)

    def starting_deal(self):
        for player in self.players:
            self.deal_card(player)
            self.deal_card(player)
            player.to_string()

    def get_winners(self, playerList):
        winners = []
        max_hand_val = -1
        for player in playerList:
            hand_val = player.calculate_hand()
            if hand_val > 21:
                continue
            if max_hand_val < hand_val:
                winners = [player.name]
            elif max_hand_val == hand_val:
                winners.append(player.name)
            curMax = max(max_hand_val,hand_val)
        return winners
             

    def print_hit(self, hand_val, player):
        if len(player.hand) == 0:
            print("this function isn't meant to be called on an empty hand")
            return 
        print(f"badabing badaboom you got a {player.hand[-1].to_string()}")
        print(hand_val)
        if hand_val > 21:
            print("busted")
        if hand_val == 21:
            print("21!")

    def print_hand(self, player):
        print(player.to_string())
        return

    def shuffle_deck(self, table_deck : Deck):
        self.table_deck.deck = self.table_deck.deck + self.used_cards.deck
        random.shuffle(self.table_deck.deck)
        return True

    def get_user_action(self, player):
        user_input = input(f"{player.name}, please input a h to hit, or s to stay")
        while user_input not in VALID_ACTIONS:
            user_input = input(f"{player.name}, please input a h to hit, or s to stay")
        return user_input

    def execute_turn(self, player):
        hand_val = player.calculate_hand()

        if hand_val == 21:
            print("21!")
            return
        while hand_val < 21:
            action = self.get_user_action(player)
            if action == "h":
                hand_val = self.player_hit(player)
                self.print_hit(hand_val, player)

            if action == "s":
                self.player_stay(player)
                self.print_hand(player)
                break
        return

    def gameLoop(self):
        self.get_players()
        self.shuffle_deck(self.table_deck)
        self.starting_deal()

        for player in self.players:
            print(player.to_string())
            self.execute_turn(player)

        print("here are the winners: ", self.get_winners(self.players))
        #self.shuffle_deck(self.tableDeck)
        #then we're going to cycle through the players asking if they want to hit, checking their card value after to see if they bust
        #then we check each players hand looking for max hand, keeping track of all the players that won

if __name__ == "__main__":
    Black().gameLoop()
"""    table = Black
    shomik = Player("shomik",[])
    table.add_player(Player("shomik"))
    table.add_player(Player("james"))
    table.dealCard(shomik)
    table.dealCard(shomik)

    hand_value = table.player_hit(shomik)
    if hand_value > 21:
        print("shomik busted xd")
    

"""
