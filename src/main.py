from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
from src.database import init_db, insert_pokemon, get_all_pokemon
from src.model import Pokemon
from fastapi import HTTPException

class PokemonCreate(BaseModel):
    name: str
    type: str

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
async def create_pokemon(pokemon_data: PokemonCreate):
    """Create a new Pokemon"""
    try:
        if not pokemon_data.name.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "errors": [{
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "Pokemon name cannot be empty"
                    }]
                }
            )

        pokemon = Pokemon(name=pokemon_data.name, type=pokemon_data.type)
        pokemon_id = insert_pokemon(pokemon)
        
        return {
            "message": "Pokemon created successfully",
            "data": {
                "id": str(pokemon_id),
                "attributes": {
                    "name": pokemon_data.name,
                    "type": pokemon_data.type
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "errors": [{
                    "status": "500",
                    "title": "Internal Server Error",
                    "detail": str(e)
                }]
            }
        )

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