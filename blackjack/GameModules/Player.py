import GameModules.Card as Card

class Player:
    def __init__(self, name : str, cards = []):
        self.name = name
        self.hand = []
        for card in cards:
            self.hand.append(card)
    
    def get_hand(self):
        deep_copy_hand = []
        for card in self.hand:
            deep_copy_hand.append(card.deep_copy())
        return deep_copy_hand

    def set_hand(self, card_list : list[Card.Card]):
        self.hand = card_list

    def did_bust(self):
        if self.calculate_hand() > 21:
            return True
        return False

    def calculate_hand(self):
        total_without_aces = self.hand_total_other_than_aces()
        aces_count = self.count_aces_in_hand()

        if aces_count >= 1 and self.total_with_one_ace_is_eleven() <= 21:
            return self.total_with_one_ace_is_eleven()
        return total_without_aces + aces_count

    def total_with_one_ace_is_eleven(self):
        total_with_ace_eleven = self.hand_total_other_than_aces() + 11
        num_other_aces = self.count_aces_in_hand() - 1
        return total_with_ace_eleven + num_other_aces

    def hand_total_other_than_aces(self):
        count = 0
        for card in self.hand:
            if not card.is_ace():
                count += card.value
        return count

    def count_aces_in_hand(self):
        count = 0
        for card in self.hand:
            if card.is_ace():
                count += 1
        return count

    def to_string(self):
        prefix_string = f"{self.name}, hand is: "
        if len(self.hand) == 0:
            return prefix_string + "empty"

        hand_string = ", ".join(self.hand_to_string())
        return  prefix_string + hand_string
    
    def hand_to_string(self):
        card_list = []
        for card in self.hand:
            card_list.append(card.to_string())
        return card_list

