from GameModules.Player import Player
from GameModules.Card import Card


class PlayerTests:
    def run_all(self):
        self.player_did_bust_test()
        self.calculate_hand_test()
        self.player_to_string_test()
        print("finished player tests")

    def player_did_bust_test(self):
        self.player_did_bust_ace()
        self.player_did_bust_no_ace()
        self.player_did_bust_no_ace()
        
    def player_did_bust_ace(self):
        assert Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("10", 10, "spades"), Card("ace", 1, "clubs")]).did_bust()

    def player_did_bust_no_ace(self):
        assert Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("10", 10, "spades"), Card("ace", 10, "hearts")]).did_bust()

    def player_did_bust_no_ace(self):
        assert not Player("andrew", [Card("10", 10, "clubs"), Card("10", 10, "diamonds")]).did_bust()

    def calculate_hand_test(self):
        self.calculate_no_ace_hands()
        self.calculate_with_ace_hands()
        self.calculate_multiple_ace_hands()

    def calculate_no_ace_hands(self):
        self.calculate_no_ace_busted()
        self.calculate_no_ace_winnable()
        
    def calculate_no_ace_busted(self):
        self.calculate_hand_helper([Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("9", 9, "hearts")], 29)
        self.calculate_hand_helper([Card("10", 10, "clubs"), Card("10", 10, "diamonds"), Card("5", 5, "hearts")], 25)

    def calculate_no_ace_winnable(self):
        self.calculate_hand_helper([Card("10", 10, "clubs"), Card("10", 10, "diamonds")], 20)
        self.calculate_hand_helper([Card("10", 10, "clubs"), Card("5", 5, "diamonds"), Card("5", 5, "hearts")], 20)

    def calculate_with_ace_hands(self):
        self.caluclate_ace_busted()
        self.calculate_ace_winnable()

    def caluclate_ace_busted(self):
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("jack", 10, "clubs"), Card("5", 5, "spades"), Card("10", 10, "spades")], 26)
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("jack", 10, "clubs"), Card("9", 9, "spades"), Card("8", 8, "spades")], 28)

    def calculate_ace_winnable(self):
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("jack", 10, "clubs"), Card("10", 10, "spades")], 21)
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("jack", 10, "clubs")], 21)

    def calculate_multiple_ace_hands(self):
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("ace", 1, "clubs"), Card("ace", 1, "hearts")], 13)
        self.calculate_hand_helper([Card("ace",1,"spades"), Card("ace", 1, "clubs")], 12)

    def calculate_hand_helper(self, hand, expected_value):
        assert Player("andrew", hand).calculate_hand() == expected_value

    def player_to_string_test(self):
        self.check_empty_hand()
        self.check_empty_name()
        self.check_multiple_cards()

    def check_empty_hand(self):
        assert(Player("andrew", []).to_string() == "andrew, hand is: empty")

    def check_empty_name(self):
        assert(Player("andrew", [Card("ace", 1, "spades")]).to_string() == "andrew, hand is: ace of spades")

    def check_multiple_cards(self):
        assert(Player("andrew", [Card("ace", 1, "spades"), Card("ace", 1, "clubs"), Card("jack", 10, "diamonds")]).to_string() == "andrew, hand is: ace of spades, ace of clubs, jack of diamonds")

        
