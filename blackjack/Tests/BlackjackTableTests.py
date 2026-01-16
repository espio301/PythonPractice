
from io import StringIO
from contextlib import redirect_stdout
from GameModules.Player import Player
from GameModules.Card import Card
from GameModules.BlackjackTable import BlackjackTable


class blackjack_table_tests:
    def run_all(self):
        self.player_hit_test()
        self.starting_deal_test()
        self.get_winners_test()
        self.print_hit_test()
        print("finished blackjack table tests")

    def player_hit_test(self):
        table = BlackjackTable()
        player = Player("andrew", [])
        table.player_hit(player)
        assert len(player.hand) == 1

    def starting_deal_test(self):
        table = self.create_table_two_players()
        table.starting_deal()
        for player in table.players:
            assert len(player.hand) == 2        

    def get_winners_test(self):
        self.check_tie()
        self.check_no_winner()
        self.check_one_winner()


    def check_tie(self):
        table = self.create_table_two_players()
        self.assign_table_hands_helper(table, [Card("ace", 1, "spades"),Card("10", 10, "spades")], [Card("ace", 1, "hearts"),Card("10", 10, "hearts")])
        player_list = table.players
        assert table.get_winners(player_list) == ["a","b"]

    def check_no_winner(self):
        table = self.create_table_two_players()
        self.assign_table_hands_helper(table, [Card("9", 9, "spades"),Card("10", 10, "spades"),Card("jack", 10, "spades")], [Card("9", 9, "hearts"),Card("10", 10, "hearts"),Card("queen", 10, "spades")])
        assert table.get_winners(table.players) == []

    def check_one_winner(self):
        table = self.create_table_two_players()
        self.assign_table_hands_helper(table, [Card("ace", 1, "spades"),Card("10", 10, "spades")], [Card("10", 10, "hearts"),Card("queen", 10, "spades")])
        assert table.get_winners(table.players) == ["a"]

    def print_hit_test(self):
        self.check_print_hit_busted()
        self.check_print_hit_not_busted()


    def check_print_hit_busted(self):
        table = self.create_table_two_players()
        player = Player("andrew", [Card("jack", 10, "spades"),Card("jack", 10, "diamonds"),Card("jack", 10, "spades")])
        output = StringIO()
        with redirect_stdout(output):
            table.print_hit(player) 
        assert output.getvalue() == "badabing badaboom you got a jack of spades\nbusted\n"

    def check_print_hit_not_busted(self):
        table = self.create_table_two_players()
        player = Player("andrew", [Card("jack", 10, "diamonds"),Card("jack", 10, "spades")])
        output = StringIO()
        with redirect_stdout(output):
            table.print_hit(player) 
        assert output.getvalue() == "badabing badaboom you got a jack of spades\n"


    def assign_table_hands_helper(self, table, hand_one, hand_two):
        #not entirely certain how to unbreak law of demeter here but im ngl kinda tired to figure it out and want to try to finish this. this is TODO
        hands_list = [hand_one, hand_two]
        for i, player in enumerate(table.players):
            player.set_hand(hands_list[i])
        

    def create_table_two_players(self):
        player_one = Player("a", [])
        player_two = Player("b", [])
        table = BlackjackTable()
        table.players = [player_one, player_two]
        return table
