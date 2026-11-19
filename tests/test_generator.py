from src.cards import Card, DrawnCard, Spread
from src.generator import generate
import pytest
def create_test_deck():
    fool = Card(
        1,
        "Шут",
        "Новое начало",
        "Необдуманность"
    )
    magician = Card(
        2,
        "Маг",
        "Сила воли и мастерство",
        "Манипуляции и обман"
    )

    high_priestess = Card(
        3,
        "Верховная Жрица",
        "Интуиция и тайные знания",
        "Скрытые мотивы и поверхностность"
    )

    empress = Card(
        4,
        "Императрица",
        "Изобилие и забота",
        "Зависимость и творческий застой"
    )
    emperor = Card(
        5,
        "Император",
        "Власть и стабильность",
        "Тирания и жесткость"
    )
    return [fool, magician, high_priestess, empress, emperor]
def test_generator():
    deck = create_test_deck()
    pattern = [{'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']}]
    gen = generate(pattern[0], deck)
    assert gen.name == 'Три периода'
    assert gen.show_count() == 3
    unique = set()
    for i in gen.show():
        unique.add(i.card.id)
    assert len(unique) == 3
def test_generator_positions():
    deck = create_test_deck()
    pattern = [{'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']}]
    gen = generate(pattern[0], deck)
    show = gen.show()
    assert show[0].position == 'Прошлое'
    assert show[1].position == 'Настоящее'
    assert show[2].position == 'Будущее'
def test_2_card():
    deck = create_test_deck()[:2]
    pattern = [{'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']}]
    with pytest.raises(ValueError):
        generate(pattern[0], deck)
def test_copy_deck():
    deck = create_test_deck()
    not_orig_deck = deck.copy()
    pattern = [{'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']}]
    generate(pattern[0], deck)
    assert deck == not_orig_deck
def test_obj():
    deck = create_test_deck()
    pattern = [{'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']}]
    gen = generate(pattern[0], deck)
    show = gen.show()
    assert isinstance(gen, Spread)
    assert all(isinstance(card, DrawnCard) for card in show)
    assert all(isinstance(card.card, Card) for card in show)
    assert all(isinstance(card.is_reversed, bool) for card in show)