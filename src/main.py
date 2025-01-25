from fastapi import FastAPI

app = FastAPI(
    title="Pokemon API",
    description="A Pokemon scraper following JSON:API standards",
    version="0.0.1"
)

@app.get("/")
async def root():
    return {"message": "Hi this is Pokemon API"}