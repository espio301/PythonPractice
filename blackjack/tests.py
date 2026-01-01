import random
import game_logic as gl
import sys
from io import StringIO
import random

random.seed(67)
SUITS_LIST = ["spades", "clubs", "hearts", "diamonds"]
RANKS_LIST = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
VALID_ACTIONS = {"s", "h"}

#we should have thorough testing for each function
class UnitTests:
    def run_all_tests(self):
        self.card_to_string_test()
        self.deck_init_test()
        self.deck_to_string_test()
        self.get_players_test()
        self.calculate_hand_test()
        self.deal_test()
        print("passed all tests!")

    def card_init_test(self):
        card = gl.Card()
        if card.suit == "" and card.number == 0 and card.numberName == "":
            return True
        raise Exception

    def to_string_face_card_test(self):
        face_card_ranks = ["ace", "jack", "queen", "king"]
        face_card_vals = [1,10,10,10]
        for i in range(0,4):
            test_card = gl.Card(face_card_ranks[i], face_card_vals[i], SUITS_LIST[i])
            assert test_card.to_string() == f"{face_card_ranks[i]} of {SUITS_LIST[i]}"
        return True

    def to_string_number_card_test(self):
        card_ranks = [str(x) for x in range(2,11)]
        card_vals = [x for x in range(2,11)]
        for i in range(0,9):
            test_card = gl.Card(card_ranks[i], card_vals[i], SUITS_LIST[i%4])
            assert test_card.to_string() == f"{card_ranks[i]} of {SUITS_LIST[i%4]}"
        return True

    def card_to_string_test(self):
        self.to_string_face_card_test()
        self.to_string_number_card_test()
        print("successfully passed all to_string tests")


    def check_card_uniqueness(self, deck):
        card_set = set()
        for card in deck:
            if card.to_string() not in card_set:
                card_set.add(card.to_string())
            else:
                return False

    def check_card_count(self, deck):
        counter = 0
        for card in deck:
            counter += 1
        return counter == 52

    def check_suit_count(self, deck):
        suitMap = {"spades": 0, "clubs": 0, "hearts": 0 , "diamonds": 0}
        for card in deck:
            if card.suit not in suitMap:
                return False
            suitMap[card.suit] += 1
        for k in suitMap:
            if suitMap[k] != 13:
                return False
        return True

    def check_rank_count(self, deck):
        rank_map = {"ace": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "jack": 0, "queen": 0, "king": 0}
        for card in deck:
            rank = card.rank
            if rank not in rank_map:
                rank_map[rank] = 0
            rank_map[rank] += 1

        for k in rank_map:
            if rank_map[k] != 4:
                return False
        return True

    #note to self: would be more readable if I just had two different maps here with distinguished names
    def check_value_correctness(self, deck):
        #value in the form of [rank's correct value, amount of times we see the value]
        number_map = {"ace" : [1,0], "2" : [2,0], "3" : [3,0], "4": [4,0], "5": [5,0], "6": [6,0], "7": [7,0], "8": [8,0], "9": [9,0], "10": [10,0], "jack": [10,0], "queen": [10,0], "king": [10,0]}
        for card in deck:
            if card.rank in number_map and number_map[card.rank][0] == card.number:
                    number_map[card.rank][1] += 1
        for k in number_map:
            if number_map[k][1] != 4:
                return False
        return True


    def deck_init_test(self):
        deck = gl.Deck().deck #definitely should rename this field
        #we can actually prove we have 1 of each card without hard coding anything by defining that each card is unique, and then that there are 13 of each suit and 4 of each card! pretty neat if you ask me :)
        assert self.check_card_count(deck) == True
        assert self.check_card_uniqueness(deck) == True
        #check suits are correct
        assert self.check_suit_count(deck) == True
        assert self.check_rank_count(deck) == True
        assert self.check_value_correctness(deck)

    def get_expected_string(self, deck : list[gl.Card]):
        prefix = f"cards in deck: {len(deck)}\n"
        card_strings = []
        for card in deck:
            card_strings.append(card.to_string())
        return prefix + ", ".join(card_strings)

    def deck_to_string_test(self):
        deck = gl.Deck().deck
        expected = self.get_expected_deck_string(deck)

        assert expected == deck.to_string()
        

    def add_two_player_test(self):
        sys.stdin.write("andrew\njames\nq\n")
        sys.stdin.seek(0)
        table.getPlayers()
        for player in table.players:
            print(player.toString())
        if table.players[0].name != "andrew" and table.players[1].name != "james":
            print("failed standard test")
            return False
        return True

    def add_no_player_test(self):
        table = gl.BlackjackTable()
        sys.stdin.write("q\n")
        sys.stdin.seek(15)
        table.getPlayers()
        if len(table.players) != 0:
            print("failed empty player list")
            return False
        return True

    def add_numerical_name(self):
        #expected value atm is for it to be ok to have numbers in names
        table = gl.BlackjackTable()
        sys.stdin.write("123\nq\n")
        sys.stdin.seek(17)
        table.getPlayers()
        if len(table.players) != 1 and table.players[0] != "123":
            print("failed empty player list")
            return False
        return True

    #need to implement if there are no players
    def get_players_test(self):
        sys.stdin = StringIO()
        table = gl.BlackjackTable()
        #standard test
        assert add_two_player_test()
        assert add_no_player_test()
        #nonstring input, technically speaking this should still pass as technically people can have numbers in their name (elons kid has non english alphabet symbols at least)
        assert add_numerical_name()
        return True
    
    def get_deck_no_aces(self):
        deck = gl.Deck().deck
        no_ace_deck = []
        for card in deck:
            if deck.rank == "ace":
                continue
            no_ace_deck.append(card)
        return no_ace_deck

    def get_deck_of_aces(self):
        aces = []
        for suit in SUITS_LIST:
            aces.append(Card("ace", 1, suit))
        return aces

    def calculate_no_ace_hand():
        no_ace_deck = self.get_deck_no_aces()
        for card in deck:
            if deck.rank == "ace":
                continue
            no_ace_deck.append(card)
        
        #hard coding 48 as if the length isn't 48 we have a different issue in deck initialization
        hand = []
        hand_value = 0
        while len(no_ace_deck) > 0:
            #we're going to get a random card from the no ace deck
            index = random.randrange(0,len(no_ace_deck))
            card = no_ace_deck[index]
            no_ace_deck.remove[index]
            #add it to the hand
            hand.append(card)

            #check if calculation is correct
            hand_value += card.value
            gl.Player("andrew", hand)
            assert hand_value == gl.Player()

        print("passed")
            
            
    #was stuck on this a bit
    def calculate_with_ace_hand(self):
        non_aces = self.get_deck_no_aces()
        aces = self.get_deck_of_aces()
        deck = gl.Deck().deck
        #create a hand with 1 ace and hand value is less than ten
        hand = []
        hand_value = 11
        non_ace_value = 0
        hand.append(aces[random.randrange(0,4)])

        while len(hand) < 20:
            index = random.randrange(0,len(deck))
            card = deck[index]
            if card.rank == "ace" and card.suit == hand[0].suit:
                deck.remove(index)
                continue
            hand.append(card)
            non_ace_value += card.value
            if non_ace_value > 10:
                hand_value -= 10
            assert Player("andrew", hand) == hand_value

    def calculate_hand_test(self):
    #check standard test
        self.calculate_no_ace_hand()
        self.calculate_with_ace_hand()
        return passed


    def empty_winners_test(self):
        table = gl.BlackjackTable()
        assert table.get_winners() == []

    def multiplayer_winners_test(self):
        num_players = random.randrange(1,11)
        table = gl.BlackjackTable()
        table.players = [Player("test player") for x in range(1,num_players)]
        for player in table.players:
            table.starting_deal(player)
        winners = []
        max_hand = 0
        for player in table.players:
            if player.calculate_hand() == max_hand:
                winners.append(player.name)
            if player.calculate_hand() > max_hand:
                max_hand = player.calculate_hand()
                winners = [player]
        assert winners == table.get_winners()

    def get_winners_test(self):
        self.empty_winners_test()
        self.multiplayer_winners_test()



    #this one's fairly important, need to check that we don't deal repeated card ever.
    #we're going to deal all 52 cards and make sure each card dealt is unique
    def deal_test(self):
        table = gl.BlackjackTable()
        p1 = gl.Player("andrew")
        while len(table.tableDeck) > 0:
            card_to_deal = deck[-1]
            card = table.deal_card(p1)
            assert card_to_deal == card
            assert card == p1.hand[-1]
        return True


    #last test is for the gameloop, which is essentially an integration test
ut = UnitTests()
#sys.stdin.write("myinput")
#sys.stdin.seek(0)  # rewind, so input() can read
#text = input()
#print(f"{text=}")
ut.run_all_tests()
print(ut.dealTest())
"""print(ut.cardInitTest())
print(ut.cardToStringTest())
#print(ut.deckInitTest())
print(ut.deckToStringTest())
"""