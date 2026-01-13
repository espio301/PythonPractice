import random


SUITS_LIST = ["spades", "clubs", "hearts", "diamonds"]
RANKS_LIST = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
VALID_ACTIONS = {"s", "h"}

#TODO: break card/deck/player into a new module
class Card:
    def __init__(self, rank : str, value : int, suit : str):
        self.rank = rank
        self.value = value
        self.suit = suit
        
    def to_string(self):
        return f"{str(self.rank)} of {str(self.suit)}"

    def is_ace(self):
        return self.rank == "ace"

class Deck:
    def __init__(self):
        self.deck = self.initialize_deck()

    def initialize_deck(self):
        deck = []
        for i, card_rank in enumerate(RANKS_LIST):
            for card_suit in SUITS_LIST:
                card_value = i + 1
                if card_value >= 10:
                    card_value = 10
                deck.append(Card(card_rank, card_value, card_suit))
        return deck

    def to_string(self):
        prefix_num_cards = f"cards in deck: {str(len(self.deck))}\n"
        decks_cards_as_string = ", ".join(self.card_strings_as_list())
        return prefix_num_cards + decks_cards_as_string

    def card_strings_as_list():
        all_cards_list = []
        for card in self.deck:
            all_cards_list.append(card.to_string())
        return all_cards_list


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
        total_without_aces = self.hand_total_other_than_aces()
        aces_count = self.count_aces_in_hand()

        if aces_count >= 1 and total_with_one_ace_is_eleven() <= 21:
            return total_with_one_ace_is_eleven()
        return total_without_aces + aces_count

    def total_with_one_ace_is_eleven():
        total_with_ace_eleven = self.hand_total_other_than_aces() + 11
        num_other_aces = self.count_aces_in_hand() - 1
        return total_with_ace_eleven + num_other_aces

    def hand_total_other_than_aces():
        count = 0
        for card in self.hand:
            if not card.is_ace():
                count += card.value
        return count

    def count_aces_in_hand():
        count = 0
        for card in self.hand():
            if card.is_ace():
                count += 1
        return count

    def to_string(self):
        prefix_string = f"{self.name}, hand is: "
        if len(self.hand) == 0:
            return prefix_string + "empty"

        hand_string = ", ".join(selfhand_to_string())
        return  prefix_string + hand_string
    
    def hand_to_string():
        card_list = []
        for card in self.hand:
            card_list.append(card.to_string())
        return card_list


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
    #TODO: theres a bug here in card_to_deal. but this will need to be refactored due to law of demeter anyways. this method is far too awarege of deck functionality. perhaps move dealing to deck instead, seems better fit for the abstraction.
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
    table = BlackjackTable()
    table.gameLoop()

