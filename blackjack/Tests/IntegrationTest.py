import sys
import random
from io import StringIO
from contextlib import redirect_stdout
from GameModules.Player import Player
from GameModules.Card import Card
from GameModules.BlackjackTable import BlackjackTable

POTENTIAL_NAMES = ["andrew", "james", "shomik", "max", "jun", "manish", "basheesh", "mm me in melee", "jane doe", "john smith"]
VALID_ACTIONS = ["h", "s"]
random.seed(80)

class IntegrationTest:

    def __init__(self):
        self.our_input = ""
        self.our_input_arr = []
        self.table = BlackjackTable()

    def run_integration_test(self):
        #BlackjackTable().game_loop()
        our_input = self.set_our_input()
        actual_output = self.get_actual_output()
        expected_output = self.get_expected_output()


    def get_expected_output(self):
        return

    def set_our_input(self):
        our_input = ""
        table = BlackjackTable()
        num_players = random.randrange(3,9)
        sys.stdin = StringIO()
        for i in range(0,num_players):
            #we're going to add random names to the std input
            rand_index = random.randint(0,len(POTENTIAL_NAMES))
            sys.stdin.write(f"{POTENTIAL_NAMES[rand_index]}\n")
            our_input += f"{POTENTIAL_NAMES[rand_index]}\n"
        
        sys.stdin.write("q\ns\n")
        our_input += "q\ns\n"
        #now we add our actions
        actions = ["s\n"]
        stay_counter = 1
        for i in range(0, random.randrange(2,9)):
            random_action = VALID_ACTIONS[random.randrange(0,2)]
            print(random_action)
            if random_action == "s":
                stay_counter += 1
            sys.stdin.write(f"{random_action}\n")
            our_input += f"{random_action}\n"
            actions.append(f"{random_action}\n")

        while stay_counter < num_players:
            print("here")
            sys.stdin.write("s\n")
            our_input += "s\n"
            stay_counter += 1
        #now we feed our input. 
        self.our_input = our_input
        self.our_input_arr = actions
        return [our_input, actions]
        
        

    def get_actual_output(self):
        output = StringIO()
        print("input", self.our_input, self.our_input_arr)
        sys.stdin.seek(0)
        with redirect_stdout(output):
        #print(inp)
#        print("that was inp")
            self.table.game_loop()
        print("game output\n", output.getvalue())
        return output



        #create 3-8 players randomly
        #have 1 person stay, then all others randomly hit 1-5 times (or until the bust of course)
        #assert the printed winners output print is correct