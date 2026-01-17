from GameModules.Deck import Deck
from GameModules.Player import Player

VALID_ACTIONS = {"s", "h"}

class BlackjackTable:
    def __init__(self):
        self.players = []
        self.table_deck = Deck()

    def player_hit(self, player: Player):
        self.deal_to(player)
        return player.calculate_hand()

    def player_stay(self, player: Player):
        return player.calculate_hand()

    def add_player(self, player: Player):
        self.players.append(player)

    #TODO could be better named
    def get_players(self):
        print("enter q to finish adding player names")
        while True:
            userInput = input("enter a name for a player (gg if your name is q): ")
            if userInput == "q":
                break
            self.add_player(Player(userInput))
        return

    def deal_to(self, player: Player):
        hand = player.get_hand()
        self.table_deck.deal_card_to(hand)
        player.set_hand(hand)

    def starting_deal(self):
        for player in self.players:
            self.deal_to(player)
            self.deal_to(player)
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
                max_hand_val = hand_val
            elif max_hand_val == hand_val:
                winners.append(player.name)
            curMax = max(max_hand_val,hand_val)
        return winners
             

    def print_hit(self, player):
        if len(player.hand) == 0:
            print("this function isn't meant to be called on an empty hand")
            return 
        print(f"badabing badaboom you got a {player.hand[-1].to_string()}")
        hand_val = player.calculate_hand()
        if hand_val > 21:
            print("busted")
        if hand_val == 21:
            print("21!")

    def print_hand(self, player):
        print(player.to_string())
        return

    def shuffle_deck(self, table_deck : Deck):
        self.table_deck.shuffle()
        return True

    def get_user_action(self, player):
        user_input = input(f"{player.name}, please input a h to hit, or s to stay\n")
        while user_input not in VALID_ACTIONS:
            user_input = input(f"{player.name}, please input a h to hit, or s to stay\n")
        return user_input

    def execute_turn(self, player):
        hand_val = player.calculate_hand()

        if hand_val == 21:
            self.print_max_hand()
            return
        while hand_val < 21:
            action = self.get_user_action(player)
            if action == "h":
                self.player_hit(player)
                self.print_hit(player)
                hand_val = player.calculate_hand()
            if action == "s":
                self.player_stay(player)
                self.print_hand(player)
                break
        return

    def print_max_hand(self):
        print("21!")

    def game_loop(self):
        self.get_players()
        self.shuffle_deck(self.table_deck)
        self.starting_deal()

        for player in self.players:
            print(player.to_string())
            self.execute_turn(player)

        print(f"here are the winners: {self.get_winners(self.players)}")

if __name__ == "__main__":
    table = BlackjackTable()
    table.game_loop()

