# we need an entry for inputs
# daily food log for a given day
    #track nutrients like protein
#given day will have a goal for protein

"""we're going to have to save the the following
    - what we eat in the day
    - what nutrients those food had
    - need to hit goal for protein
"""

#store everything to a json object

class food:
    def __init__(self):
        self.protein = 0
        self.calories = 0

class day:
    def __init(self):
        self.target = 0
        self.totalCals = 0

#while our target protein isnt hit, we need to continuously take input of foods
class calorieTracker:
    def __init__(self):
        self.foodMap = {}

    def trackLoop:
        while input from user isn't done
            take input
            if its a new food, add it to the map
            track the food
            if we hit the goal, notify the user
        tell the user his stats