class Pokemon:
    def __init__(self, name: str, types: list[str]):
        self.name = name
        self.types = types

    def get_name(self) -> str:
        return self.name

    def get_types(self) -> list[str]:
        return self.types
