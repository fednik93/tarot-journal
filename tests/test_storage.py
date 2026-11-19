import sqlite3

import pytest

from src.storage import init_db, save_reading, get_reading, get_user_readings
from src.deck import create_deck
from src.generator import generate
from src.cards import Reading, Spread, Card, DrawnCard
def test_save_reading(tmp_path):
    db_path = tmp_path / 'test.db'
    init_db(db_path)
    deck = create_deck()
    pattern = [{'name': 'Карта дня', 'positions': ['Карта дня']},
               {'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']},
               {'name': 'Выбор', 'positions': ['Вариант А', 'Вариант Б']}]
    spread = generate(pattern[1], deck)
    reading_id = save_reading(123456, spread, 'Какое будущее у меня?', db_path=db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    row = cur.execute('SELECT user_id, name, question, note FROM readings WHERE id = ?;', (reading_id,)).fetchone()
    assert row is not None
    assert row == (123456, 'Три периода', 'Какое будущее у меня?', None)
    conn.close()
def test_reading_cards(tmp_path):
    db_path = tmp_path / 'test.db'
    init_db(db_path)
    deck = create_deck()
    pattern = [{'name': 'Карта дня', 'positions': ['Карта дня']},
               {'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']},
               {'name': 'Выбор', 'positions': ['Вариант А', 'Вариант Б']}]
    spread = generate(pattern[1], deck)
    reading_id = save_reading(123456, spread, 'Какое будущее у меня?', db_path=db_path)
    reading_card = get_reading(reading_id, deck, db_path)
    assert isinstance(reading_card, Reading)
    assert isinstance(reading_card.spread, Spread)
    assert all(isinstance(card, DrawnCard) for card in reading_card.spread.cards)
    assert all(isinstance(drawn_card.card, Card) for drawn_card in reading_card.spread.cards)
    assert len(reading_card.spread.cards) == len(spread.cards)
    for first, second in zip(reading_card.spread.cards, spread.cards):
        assert first.card.id == second.card.id
        assert first.position == second.position
        assert first.is_reversed == second.is_reversed
    assert reading_card.id == reading_id
    assert reading_card.user_id == 123456
    assert reading_card.question == 'Какое будущее у меня?'
    assert reading_card.note is None
    assert reading_card.created_at is not None
def test_get_missing_reading(tmp_path):
    db_path = tmp_path / 'test_db'
    init_db(db_path)
    deck = create_deck()
    with pytest.raises(ValueError):
        get_reading(123, deck, db_path)
def test_get_user_readings(tmp_path):
    db_path = tmp_path / 'test_db'
    init_db(db_path)
    deck = create_deck()
    pattern = [{'name': 'Карта дня', 'positions': ['Карта дня']},
               {'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']},
               {'name': 'Выбор', 'positions': ['Вариант А', 'Вариант Б']}]
    spread = generate(pattern[1], deck)
    first1 = save_reading(123, spread, 'Какое будущее у меня?1', db_path=db_path)
    first2 = save_reading(123, spread, 'Какое будущее у меня?2', db_path=db_path)
    second = save_reading(456, spread, 'Какое будущее у меня?456', db_path=db_path)
    res = get_user_readings(123, db_path)
    assert len(res) == 2
    assert [row[0] for row in res] == [first2, first1]
    assert [row[2] for row in res] == ['Какое будущее у меня?2', 'Какое будущее у меня?1']