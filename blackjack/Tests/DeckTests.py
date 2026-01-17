#a note to self, when I write classes, I should really just write getters and setters immediately. yes I know comments are bad but if writing this helps me remember this lesson for later then thats worth it
from logging import raiseExceptions
from GameModules import Deck as gm
import random

random.seed(67)

class DeckTests:

    def run_all(self):
        self.deck_init_test()
        self.deck_to_string_test()
        self.deck_deal_test()
        self.deck_shuffle_test()
        print("finished deck tests")

    def deck_init_test(self):
        deck = gm.Deck().deck
        #we can actually prove we have 1 of each card without hard coding anything by defining that each card is unique, and then that there are 13 of each suit and 4 of each card! pretty neat if you ask me :)
        self.check_card_count(deck)
        self.check_card_uniqueness(deck)
        self.check_suit_correctness(deck)
        self.check_rank_count(deck)
        self.check_value_correctness(deck)


    def check_card_count(self, deck):
        counter = 0
        for card in deck:
            counter += 1
        assert counter == 52

    def check_card_uniqueness(self, deck):
        card_set = set()
        for card in deck:
            if card.to_string() not in card_set:
                card_set.add(card.to_string())
            else:
                raise Exception('failed uniqueness check')

    def check_suit_correctness(self, deck):
        suitMap = {"spades": 0, "clubs": 0, "hearts": 0 , "diamonds": 0}
        for card in deck:
            if card.suit not in suitMap:
                raise Exception('failed suit count check, one suit isnt amongs spades, clubs, hearts or diamonds.')
            suitMap[card.suit] += 1
        for k in suitMap:
            if suitMap[k] != 13:
                raise Exception('failed suit count check, one suit totalled to not having 13 cards')

    def check_rank_count(self, deck):
        deck_obj = gm.Deck()
        rank_map = self.map_decks_ranks(deck_obj.deck)
        assert self.check_rank_map_correctness(rank_map)

    def map_decks_ranks(self,deck):
        rank_map = {"ace": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "jack": 0, "queen": 0, "king": 0}
        for card in deck:
            rank = card.rank
            if rank not in rank_map:
                rank_map[rank] = 0
            rank_map[rank] += 1
        return rank_map

    def check_rank_map_correctness(self, rank_map):
        for k in rank_map:
            if rank_map[k] != 4:
                return False
        return True

    def check_value_correctness(self, deck):
        rank_count_map = self.check_rank_value_correctness(deck)
        self.check_value_count_correctness(rank_count_map)

    def check_rank_value_correctness(self, deck):
        rank_value_map = {"ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "jack":10, "queen":10, "king":10}
        correct_ranks_seen = {"ace":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "jack":0, "queen":0, "king":0}
        for card in deck:
            if card.value != rank_value_map[card.rank]:
                raise Exception('failed there exists a card with incorrect rank to value assignment')
            correct_ranks_seen[card.rank] += 1
        return correct_ranks_seen

    def check_value_count_correctness(self, rank_count_map):
        for rank in rank_count_map:
            if rank_count_map[rank] != 4:
                raise Exception(f"one value, {rank_count_map[rank]} has an improper amount for it's rank, {rank}")

    def deck_to_string_test(self):
        deck_obj = gm.Deck()
        assert self.get_expected_string() == deck_obj.to_string()

    def get_expected_string(self):
        deck = gm.Deck().deck
        prefix = f"cards in deck: {len(deck)}\n"
        card_strings = []
        for card in deck:
            card_strings.append(card.to_string())
        return prefix + ", ".join(card_strings)

    def deck_deal_test(self):
        deck_obj = gm.Deck()
        player_hand = []
        while len(deck_obj.deck) > 0:
            deck_obj.deal_card_to(player_hand)
            self.check_player_hand(player_hand, deck_obj)
            self.check_dealt_card_not_in_deck(deck_obj)

    def check_player_hand(self, player_hand, deck_obj):
        card_dealt = deck_obj.used_cards[-1]
        assert deck_obj.used_cards[-1] == card_dealt
        
    def check_dealt_card_not_in_deck(self, deck_obj):
        dealt_card = deck_obj.used_cards[-1]
        for card in deck_obj.deck:
            if dealt_card == card:
                raise Exception("found the dealt card inside our deck")

    def deck_shuffle_test(self):
        shuffled_obj = gm.Deck()
        shuffled_obj.shuffle()
        unshuffled_deck = gm.Deck().deck

        self.check_used_cards(shuffled_obj)
        for i in range(0,52):
            num_cards_in_same_place = 0
            if shuffled_obj.deck[i].to_string() == unshuffled_deck[i].to_string():
                num_cards_in_same_place += 1
        assert num_cards_in_same_place != 52

    def check_used_cards(self, deck_obj):
        if len(deck_obj.used_cards) > 0:
            raise Exception("there are cards in used_cards after shuffling")
