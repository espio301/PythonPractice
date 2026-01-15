import Card
import random

SUITS_LIST = ["spades", "clubs", "hearts", "diamonds"]
RANKS_LIST = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

class Deck:
    def __init__(self):
        self.deck = self.initialize_deck()
        self.used_cards = []

    def initialize_deck(self):
        deck = []
        for i, card_rank in enumerate(RANKS_LIST):
            for card_suit in SUITS_LIST:
                card_value = i + 1
                if card_value >= 10:
                    card_value = 10
                deck.append(Card.Card(card_rank, card_value, card_suit))
        return deck

    def to_string(self):
        prefix_num_cards = f"cards in deck: {str(len(self.deck))}\n"
        decks_cards_as_string = ", ".join(self.card_strings_as_list())
        return prefix_num_cards + decks_cards_as_string

    def deal_card_to(self, card_list):
        card = self.deck.pop()
        card_list.append(card)
        self.used_cards.append(card)
        return card_list

    def shuffle(self):
        self.deck.extend(self.used_cards)
        self.used_cards = []
        for i in range(0,len(self.deck)):
            index_card = self.deck[i]
            random_index = random.randrange(0,len(self.deck))
            swap_card = self.deck[random_index]
            self.deck[random_index] = index_card
            self.deck[i] = swap_card

    def card_strings_as_list():
        all_cards_list = []
        for card in self.deck:
            all_cards_list.append(card.to_string())
        return all_cards_list
