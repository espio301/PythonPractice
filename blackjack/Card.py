class Card:
    def __init__(self, rank : str, value : int, suit : str):
        self.rank = rank
        self.value = value
        self.suit = suit
        
    def deep_copy(self):
        return Card(self.rank, self.value, self.suit)

    def to_string(self):
        return f"{str(self.rank)} of {str(self.suit)}"

    def is_ace(self):
        return self.rank == "ace"