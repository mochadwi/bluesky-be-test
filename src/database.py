import json
import sqlite3
from contextlib import contextmanager
from src.model import Pokemon

DATABASE_URL = "pokemon.db"

def init_db():
    with get_db() as db:
        # Create Pokemon table
        db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        
        db.execute("""
        CREATE TABLE IF NOT EXISTS types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        
        # Pokemon-Types junction table
        db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_types (
            pokemon_id INTEGER,
            type_id INTEGER,
            slot INTEGER NOT NULL,
            PRIMARY KEY (pokemon_id, type_id),
            FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
            FOREIGN KEY (type_id) REFERENCES types (id)
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
        try:
            cursor = db.execute(
                "INSERT INTO pokemon (name) VALUES (?)",
                (pokemon.get_name())
            )
            pokemon_id = cursor.lastrowid
            
            # Insert or get types and create relationships
            for i, type_name in enumerate(pokemon.get_types(), 1):
                # Insert or get type
                db.execute(
                    "INSERT OR IGNORE INTO types (name) VALUES (?)",
                    (type_name,)
                )
                cursor = db.execute(
                    "SELECT id FROM types WHERE name = ?",
                    (type_name,)
                )
                type_id = cursor.fetchone()['id']
                
                # Create relationship
                db.execute(
                    "INSERT INTO pokemon_types (pokemon_id, type_id, slot) VALUES (?, ?, ?)",
                    (pokemon_id, type_id, i)
                )
            
            db.commit()
            return pokemon_id
        except sqlite3.IntegrityError:
            db.rollback()
            raise ValueError(f"Pokemon with name {pokemon.get_name()} already exists")

def get_all_pokemon():
    with get_db() as db:
        cursor = db.execute("""
            SELECT p.id, p.name, GROUP_CONCAT(t.name) as types
            FROM pokemon p
            LEFT JOIN pokemon_types pt ON p.id = pt.pokemon_id
            LEFT JOIN types t ON pt.type_id = t.id
            GROUP BY p.id, p.name
        """)
        rows = cursor.fetchall()
        return [{
            'type': 'pokemon',
            'id': str(row['id']),
            'attributes': {
                'name': row['name'],
                'types': row['types'].split(',') if row['types'] else []
            }
        } for row in rows]