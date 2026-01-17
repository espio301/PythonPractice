from GameModules import Card as gm

class card_tests:
    def run_all(self):
        self.deep_copy_test()
        self.to_string_test()
        self.is_ace_test()
        print("finished card tests")

    def deep_copy_test(self):
        card_to_change = gm.Card("ace", 1, "clubs")
        deep_copy = card_to_change.deep_copy()
        card_to_change.suit = "diamonds"
        print()
        assert deep_copy.suit == "clubs" and card_to_change.suit == "diamonds"

    def to_string_test(self):
        card = gm.Card("ace", 1, "clubs")
        assert card.to_string() == "ace of clubs"

    def is_ace_test(self):
        self.test_on_ace()
        self.test_not_on_ace()

    def test_on_ace(self):
        card = gm.Card("ace", 1, "clubs")
        assert card.is_ace()

    def test_not_on_ace(self):
        card = gm.Card("5", 5, "diamonds")
        assert not card.is_ace()