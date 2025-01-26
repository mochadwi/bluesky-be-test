class PokemonType:
    def __init__(self, name: str, slot: int):
        self.name = name
        self.slot = slot

    def get_name(self) -> str:
        return self.name

    def get_slot(self) -> int:
        return self.slot

class Pokemon:
    def __init__(self, name: str, types: list[PokemonType]):
        self.name = name
        self.types = types

    def get_name(self) -> str:
        return self.name

    def get_types(self) -> list[PokemonType]:
        return self.types