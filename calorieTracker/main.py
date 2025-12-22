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
import json

def dayEncoder(obj):
    if isinstance(obj, day):
        return obj.__dict__
    raise TypeError()

class food:
    def __init__(self, protein = 0, calories = 0):
        self.protein = protein
        self.calories = calories

class day:
    def __init__(self):
        self.targetProtein = 0
        self.totalCalories = 0
        self.dayName = ""
        self.totalProtein = 0

#while our target protein isnt hit, we need to continuously take input of foods
class calorieTracker:
    def __init__(self):
        self.foodMap = {}
        self.Day = day()

    def trackDay(self):
        curDay = self.Day
        curDay.dayName = input("what day of the week is it: ")
        print("enter q to stop tracker for the day")
        curCalories = 0
        curProtein = 0
        while True:
            userInput = input("input the food you just ate: ")
            if userInput == "q":
                break
            if userInput.lower() not in self.foodMap:
                print("this food isnt in the map, please enter the following nutrient for it")
                foodProtein = int(input("\n protein in grams: "))
                foodCalories = int(input("\n how many calories: "))
                self.foodMap[userInput.lower()] = food(foodProtein, foodCalories)
        
            curProtein += self.foodMap[userInput.lower()].protein
            curCalories += self.foodMap[userInput.lower()].calories
            print(f"current Protein is {curProtein} and our current calories is {curCalories}")
        curDay.totalProtein = curProtein
        curDay.totalCalories = curCalories
        print(curDay)
        print(f"on {curDay.dayName} we have gotten a total of {curDay.totalProtein}g of protein, and {curDay.totalCalories} calories")
        print(json.dumps(curDay, default=dayEncoder))


"""        while input from user isn't done
            take input
            if its a new food, add it to the map
            track the food
            if we hit the goal, notify the user
        tell the user his stats"""

tracker = calorieTracker()
tracker.trackDay()