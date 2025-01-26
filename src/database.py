import sqlite3
from contextlib import contextmanager
from src.model import Pokemon

DATABASE_URL = "pokemon.db"

def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL
        )
        """)
        db.commit()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def insert_pokemon(pokemon: Pokemon):
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO pokemon (name, type) VALUES (?, ?)",
            (pokemon.get_name(), pokemon.get_type())
        )
        db.commit()
        return cursor.lastrowid

def get_all_pokemon():
    with get_db() as db:
        cursor = db.execute("SELECT * FROM pokemon")
        return [dict(row) for row in cursor.fetchall()]