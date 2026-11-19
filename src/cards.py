class Card:
    def __init__(self, id, name, upright_meaning, reversed_meaning):
        self.id = id
        self.name = name
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
    def get_meaning(self, is_reversed):
        return self.reversed_meaning if is_reversed else self.upright_meaning
class DrawnCard:
    def __init__(self, card, position, is_reversed):
        self.card = card
        self.position = position
        self.is_reversed = is_reversed
    def get_meaning(self):
        return self.card.get_meaning(self.is_reversed)
class Spread:
    def __init__(self, name, cards=None):
        self.name = name
        self.cards = list(cards) if cards is not None else []
    def add_card(self, card):
        self.cards.append(card)
    def show(self):
        return [card for card in self.cards]
    def show_count(self):
        return len(self.cards)
class Reading():
    def __init__(self, id, user_id, spread, question, note, created_at):
        self.id = id
        self.user_id = user_id
        self.spread = spread
        self.question = question
        self.note = note
        self.created_at = created_at