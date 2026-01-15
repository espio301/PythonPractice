from GameModules.Player import Player
from GameModules.Card import Card


class player_tests:
    def run_all(self):
        self.player_did_bust_test()
        print("finished player tests")

    def player_did_bust_test(self):
        self.check_did_bust_ace()
        self.check_did_bust_no_ace()
        self.check_didnt_bust()
        
    def player_did_bust_ace(self):
        assert Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("10", 10, "spades"), Card("ace", 1, "clubs")]).did_bust()

    def player_did_bust_no_ace(self):
        assert Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("10", 10, "spades"), Card("ace", 10, "hearts")]).did_bust()

    def player_did_bust_no_ace(self):
        assert not Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds")]).did_bust()

    def calculate_hand_test(self):
    #check standard test
        self.calculate_no_ace_hand()
        self.calculate_with_ace_hand()
        return passed

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


        def player_to_string_test(self):
            self.check_empty_hand()
            self.check_empty_name()
            self.check_multiple_cards()
            assert Player("Andrew")

        def check_empty_hand(self):
            assert(Player("andrew", [])).to_string == "andrew, hand is empty"

        def check_empty_name(self):
            assert(Player("andrew", [Card("ace", 1, "spades")])).to_string == ", hand is ace of spades"

        def check_multiple_cards(self):
            assert(Player("andrew", [Card("ace", 1, "spades"), Card("ace", 1, "clubs"), Card("jack", 10, "diamonds")])).to_string == "andrew, hand is ace of spades, ace of clubs, jack of diamonds"

        
