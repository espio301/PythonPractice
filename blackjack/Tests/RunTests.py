from Tests import CardTests
from Tests import DeckTests
from Tests import PlayerTests
from Tests import BlackjackTableTests
from Tests import IntegrationTest
import sys
from io import StringIO
from contextlib import redirect_stdout

#TODO PEP 8 has CapWords for classnames, should fix this
def run_tests():
    card_tests = CardTests.card_tests()
    deck_tests = DeckTests.deck_tests()
    player_tests = PlayerTests.player_tests()
    blackjack_table_tests = BlackjackTableTests.blackjack_table_tests()

    card_tests.run_all()
    deck_tests.run_all()
    player_tests.run_all()
    blackjack_table_tests.run_all()
    print("finished all unit tests")


def run_integration_test():
    integration_test = IntegrationTest.IntegrationTest()
    integration_test.run_integration_test()

run_integration_test()
run_tests()