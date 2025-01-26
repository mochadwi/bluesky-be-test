import httpx
from typing import Dict, List
from src.model import Pokemon
from src.database import insert_pokemon

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

    async def fetch_pokemon_details(self, id: int) -> Dict:
        """Fetch detailed information of a Pokemon.
        Args:
            id (int): ID of the Pokemon
        Returns:
            Dict: Detailed information of the Pokemon including types
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/pokemon/{id}"
            )
            response.raise_for_status()
            data = response.json()
            return {
                "name": data["name"],
                "types": [t["type"]["name"] for t in data["types"]]
            }
        except httpx.HTTPError as e:
            print(f"Error fetching Pokemon details: {e}")
            return {}

    async def scrape_and_store(self, limit: int = 100):
        """Main function to scrape Pokemon data and store in database"""
        pokemon_list = await self.fetch_pokemon_list(limit=limit)
        
        for pokemon in pokemon_list:
            try:
                pokemon_id = int(pokemon["url"].split("/")[-2])
                pokemon_details = await self.fetch_pokemon_details(pokemon_id)
                if pokemon_details:
                    pokemon_obj = Pokemon(
                        name=pokemon_details["name"],
                        types=pokemon_details["types"]
                    )
                insert_pokemon(pokemon_obj)
                print(f"Successfully stored {pokemon}")
            except Exception as e:
                print(f"Error processing {pokemon.get('name', 'unknown')}: {e}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
