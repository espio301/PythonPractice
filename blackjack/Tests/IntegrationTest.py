import sys
import random
from io import StringIO
from contextlib import redirect_stdout
from GameModules.Player import Player
from GameModules.Card import Card
from GameModules.BlackjackTable import BlackjackTable

POTENTIAL_NAMES = ["andrew", "james", "shomik", "max", "jun", "manish", "basheesh", "mm me in melee", "jane doe", "john smith"]
VALID_ACTIONS = ["h", "s"]
random.seed(67)
#note to self seed 68 actually has some useful edge cases, worth also using that seed

class IntegrationTest:

    def __init__(self):
        self.our_names_arr = []
        self.our_actions_arr = []
        self.table = BlackjackTable()

    def run_integration_test(self):
        self.set_our_input()        
        assert self.get_actual_output() == self.get_expected_output()


    def get_expected_output(self):
        expected_output = self.add_expected_naming_output() + self.add_expected_hit_stay_output() + self.add_get_winners_output() + "\n"
        return expected_output


    def add_expected_naming_output(self):
        expected_out = "enter q to finish adding player names\n"
        for name in self.our_names_arr:
            expected_out += "enter a name for a player (gg if your name is q): "
        statement_when_quitting = "enter a name for a player (gg if your name is q): "
        return expected_out + statement_when_quitting

    #it's possible I'm tired, but I think I could use some tips on refactoring something like this. Its similar to a fsm and because it has a few different states to keep track of, seems a bit harder to break down without having some kind of object to hold the state. But idt that should change the readability so much??
    def add_expected_hit_stay_output(self):
        expected_output = ""
        action_index = 0
        current_amt_cards = 2
        player_index = 0
        is_new_player = True

        while player_index < len(self.table.players):
            player = self.table.players[player_index]
            if is_new_player:
                expected_output += self.write_expected_for_new_player(player)
                is_new_player = False
                current_amt_cards = 2

            hand_val = self.get_value_of_hand(player, current_amt_cards)
            if hand_val == 21:
                expected_output += "21!\n"
                player_index += 1
                is_new_player = True
                continue

            expected_output += f"{player.name}, please input a h to hit, or s to stay\n"
            action = self.our_actions_arr[action_index]

            if action == "s\n":
                expected_output += f"{player.to_string()}\n"
                player_index += 1
                is_new_player = True

            if action == "h\n":
                current_amt_cards += 1
                expected_output += self.write_expected_hit(player, current_amt_cards)
                if self.get_value_of_hand(player, current_amt_cards) >= 21:
                    player_index += 1
                    is_new_player = True

            action_index += 1
            
        return expected_output

    def write_expected_hit(self, player, current_amt_cards):
        player_hand = player.get_hand()
        new_card = player_hand[current_amt_cards-1]
        expected_output = f"badabing badaboom you got a {new_card.to_string()}\n"
        hand_val = self.get_value_of_hand(player, current_amt_cards)

        if hand_val == 21:
            expected_output += "21!\n"
        if hand_val > 21:
            expected_output += "busted\n"
        return expected_output

    def write_expected_for_new_player(self, player):
        player_end_state_hand = player.get_hand()
        player_helper = Player(player.name, [player_end_state_hand[0], player_end_state_hand[1]])
        return f"{player_helper.to_string()}\n"

    def get_value_of_hand(self, player, number_of_cards):
        player_helper = Player("", player.get_hand()[:number_of_cards])
        return player_helper.calculate_hand()


    def add_get_winners_output(self):
        players = self.table.players
        return f"here are the winners: {self.table.get_winners(players)}"
            
    def set_our_input(self):
        self.initialize_stdin()
        self.write_names_to_input()
        self.write_quit_signal()
        self.write_actions()
        self.write_minimum_needed_stay_actions()

    def initialize_stdin(self):
        sys.stdin = StringIO()

    def write_quit_signal(self):
        sys.stdin.write("q\n")
    
    def write_guaranteed_stay_action(self):
        sys.stdin.write("s\n")
        self.our_actions_arr.append("s\n")

    def write_actions(self):
        self.write_guaranteed_stay_action()
        stay_counter = 1
        for i in range(0, random.randrange(2,9)):
            random_action = VALID_ACTIONS[random.randrange(0,2)]
            #print(random_action)
            if random_action == "s":
                stay_counter += 1
            sys.stdin.write(f"{random_action}\n")
            self.our_actions_arr.append(f"{random_action}\n")

    def write_minimum_needed_stay_actions(self):
        stay_counter = 0
        num_names = len(self.our_names_arr)
        for action in self.our_actions_arr:
            if action == "s\n":
                stay_counter += 1
        
        while stay_counter < num_names:
            sys.stdin.write("s\n")
            self.our_actions_arr.append("s\n")
            stay_counter += 1


    def write_names_to_input(self):
        num_players = random.randrange(3,9)
        for i in range(0,num_players):
            #we're going to add random names to the std input
            rand_index = random.randint(0,len(POTENTIAL_NAMES))
            sys.stdin.write(f"{POTENTIAL_NAMES[rand_index]}\n")
            self.our_names_arr.append(POTENTIAL_NAMES[rand_index])
        return num_players


    def get_actual_output(self):
        output = StringIO()
        sys.stdin.seek(0)
        with redirect_stdout(output):
            self.table.game_loop()
        return output.getvalue()
