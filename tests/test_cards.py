from src.cards import Card, DrawnCard, Spread
def test_upp():
    card = Card(1, "Шут",  "Новое начало", "Необдуманность")
    assert card.get_meaning(False) == "Новое начало"
def test_revert():
    card = Card(1, "Шут",  "Новое начало", "Необдуманность")
    assert card.get_meaning(True) == "Необдуманность"
def test_drawn_card():
    card = Card(1, "Шут",  "Новое начало", "Необдуманность")
    drawn = DrawnCard(card, 'Прошлое', True)
    assert card.name == "Шут"
    assert card.reversed_meaning == "Необдуманность"
    assert drawn.get_meaning() == 'Необдуманность'
    assert drawn.card is card
    assert drawn.is_reversed is True
    assert drawn.position == 'Прошлое'
def test_spread_add_card_and_count():
    spread = Spread('Карта дня')
    card = Card(1, "Шут",  "Новое начало", "Необдуманность")
    drawn = DrawnCard(card, 'карта дня', True)
    spread.add_card(drawn)
    assert spread.show()[0].card.name == "Шут"
    assert spread.show_count() == 1
def test_spread_independence():
    spread1 = Spread('Карта дня')
    spread2 = Spread('Выбор')
    card = Card(1, "Шут", "Новое начало", "Необдуманность")
    drawn = DrawnCard(card, 'карта дня', True)
    spread1.add_card(drawn)
    assert spread2.show_count() == 0
    assert spread1.show_count() == 1