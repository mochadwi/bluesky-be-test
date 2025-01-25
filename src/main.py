from fastapi import FastAPI
from typing import Dict
from database import init_db, insert_pokemon
from model import Pokemon

app = FastAPI(
    title="Pokemon API",
    description="Basic Pokemon API",
    version="0.0.1"
)

@app.on_event("startup")
async def startup_event():
    # Initialize the database
    init_db()

@app.get("/")
async def root():
    return {"message": "Hi this is Pokemon API"}

@app.post("/api/pokemon", response_model=Dict)
async def create_pokemon(name: str, type: str):
    """Create a new Pokemon"""
    pokemon = Pokemon(name=name, type=type)
    pokemon_id = insert_pokemon(pokemon)
    
    return {
        "message": "Pokemon created successfully",
        "data": {
            "id": str(pokemon_id),
            "attributes": {
                "name": name,
                "type": type
            }
        }
    }

@app.get("/api/pokemon", response_model=Dict)
async def get_pokemon():
    """Get all Pokemon"""
    pokemon_list = get_all_pokemon()
    return {
        "message": "Pokemon retrieved successfully",
        "data": [
            {
                "id": str(pokemon["id"]),
                "attributes": {
                    "name": pokemon["name"],
                    "type": pokemon["type"]
                }
            } for pokemon in pokemon_list
        ]
    }