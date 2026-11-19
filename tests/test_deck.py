from src.cards import Card
from src.deck import create_deck
def test_deck():
    deck = create_deck()
    assert len(deck) == 22
    assert all(isinstance(card, Card) for card in deck)
    unique = set()
    for i in deck:
        unique.add(i.id)
    assert len(unique) == 22