from .storage import init_db, save_reading, get_reading
from .generator import generate
from .deck import create_deck
import sqlite3
deck = create_deck()
pattern = [{'name': 'Карта дня', 'positions': ['Карта дня']},
           {'name': 'Три периода', 'positions': ['Прошлое', 'Настоящее', 'Будущее']},
           {'name': 'Выбор', 'positions': ['Вариант А', 'Вариант Б']}]
spread = generate(pattern[1], deck)
init_db()

conn = sqlite3.connect('data/tarot_db')
cur = conn.cursor()
#save_reading(123456, spread, 'Какое будущее 3')
restored1 = get_reading(5, deck)
print(restored1.id)
print(restored1.user_id)
print(restored1.spread)
print(restored1.created_at)
conn.close()