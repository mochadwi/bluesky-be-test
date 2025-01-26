import httpx
import asyncio
from typing import Dict, List
from model import Pokemon
from database import insert_pokemon

class PokemonScraper:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.client = httpx.AsyncClient(
            headers={"User-Agent": "Pokemon-Scraper/1.0"},
            timeout=30.0
        )

    async def fetch_pokemon_list(self, limit: int = 100) -> List[Dict]:
        """Fetch a list of all Pokemon.
        Args:
            limit (int): Maximum number of Pokemon to fetch
        Returns:
            List[Dict]: A list of Pokemon with basic information
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/pokemon",
                params={"limit": limit}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except httpx.HTTPError as e:
            print(f"Error fetching Pokemon list: {e}")
            return []

    async def scrape_and_store(self):
        """Main function to scrape Pokemon data and store in database"""
        pokemon_list = await self.fetch_pokemon_list()
        
        for pokemon in pokemon_list:
            try:
                pokemon_obj = Pokemon(
                    name=pokemon["name"],
                    type="todo fetch type details later"
                )
                insert_pokemon(pokemon_obj)
                print(f"Successfully stored {pokemon}")
            except Exception as e:
                print(f"Error processing {pokemon.get('name', 'unknown')}: {e}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def main():
    scraper = PokemonScraper()
    try:
        await scraper.scrape_and_store()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())