from fastapi import FastAPI
from typing import Dict
from database import init_db, create_pokemon

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
    create_pokemon(name, type)
    return { 
        "message': 'Pokemon created successfully,"
        "data": NULL
    }