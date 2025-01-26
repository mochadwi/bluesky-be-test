from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
from src.database import init_db, get_all_pokemon
from src.model import Pokemon
from src.scraper import PokemonScraper
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

@app.post("/api/pokemon/scrape")
async def scrape_pokemon(limit: int = 100):
    """Trigger Pokemon scraping"""
    scraper = PokemonScraper()
    try:
        await scraper.scrape_and_store(limit=limit)
        return {"message": "Pokemon data scraped successfully"}
    finally:
        await scraper.close()

@app.get("/api/pokemon", response_model=Dict)
async def get_pokemon():
    """Get all Pokemon"""
    return {
        "message": "Pokemon retrieved successfully",
        "data": get_all_pokemon()
    }