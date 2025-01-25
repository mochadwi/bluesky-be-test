import sqlite3
from contextlib import contextmanager

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

def create_pokemon(name: str, type: str):
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO pokemon (name, type) VALUES (?, ?)",
            (name, type)
        )
        db.commit()
        return cursor.lastrowid