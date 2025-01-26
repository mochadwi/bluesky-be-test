class PokemonType:
    def __init__(self, id: int, name: str, slot: int):
        self.id = id
        self.name = name
        self.slot = slot

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_slot(self) -> int:
        return self.slot

class Pokemon:
    def __init__(self, id: int, name: str, types: list[PokemonType]):
        self.id = id
        self.name = name
        self.types = types

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_types(self) -> list[PokemonType]:
        return self.types