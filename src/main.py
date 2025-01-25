from fastapi import FastAPI
from typing import Dict
from database import init_db

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