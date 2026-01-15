from Tests import CardTests
from Tests import DeckTests

def run_tests():
    card_tests = CardTests.card_tests()
    deck_tests = DeckTests.deck_tests()
    card_tests.run_all()
    deck_tests.run_all()

run_tests()