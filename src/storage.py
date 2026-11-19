import sqlite3
from src.cards import Spread, DrawnCard, Reading
def init_db(db_path='data/tarot_db'):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('PRAGMA foreign_keys = ON')
        cur = conn.cursor()
        cur.execute('''
            Create table if not exists readings (
                id Integer primary key,
                user_id integer not null,
                name text not null,
                question text not null,
                note TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('''
            Create table if not exists reading_cards (
                id integer primary key,
                reading_id INTEGER NOT NULL,
                card_id integer not null,
                position text not null,
                is_reversed INTEGER NOT NULL CHECK (is_reversed IN (0, 1)),
                position_order integer,
                FOREIGN KEY (reading_id) REFERENCES readings(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
    finally:
        conn.close()
def save_reading(user_id, spread, question, note=None, db_path='data/tarot_db'):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('PRAGMA foreign_keys = ON')
        cur = conn.cursor()
        cur.execute('''
            Insert into readings (user_id, name, question, note, created_at)
            values (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, spread.name, question, note))
        reading_id = cur.lastrowid
        for order, i in enumerate(spread.cards, start=1):
            cur.execute('''
                Insert into reading_cards (reading_id, card_id, position, is_reversed, position_order)
                values (?, ?, ?, ?, ?)
            ''', (reading_id, i.card.id, i.position, i.is_reversed, order))
        conn.commit()
    finally:
        conn.close()
    return reading_id
def get_reading(reading_id, deck, db_path='data/tarot_db'):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute('select name from readings where id = ?', (reading_id,))
        row = cur.fetchone()
        if row:
            spread = Spread(row[0])
        else:
            raise ValueError("Нет такого расклада")
        for row in cur.execute('select * from reading_cards where reading_id = ? ORDER BY position_order', (reading_id,)):
            card = None
            for i in deck:
                if row[2] == i.id:
                    card = i
                    break
            if card is None:
                raise ValueError("Карты не существует")
            drawn = DrawnCard(card, row[3], bool(row[4]))
            spread.add_card(drawn)
        main_data = cur.execute('select id, user_id, question, note, created_at from readings where id = ?', (reading_id,)).fetchone()
        result = Reading(main_data[0], main_data[1], spread, main_data[2], main_data[3], main_data[4])
    finally:
        conn.close()
    return result
def get_user_readings(user_id, db_path='data/tarot_db'):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        result = []
        for row in cur.execute('select id, name, question, created_at from readings where user_id = ? order by created_at DESC, id DESC', (user_id,)):
            result.append(row)
    finally:
        conn.close()
    return result