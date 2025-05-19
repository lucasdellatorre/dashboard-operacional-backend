class NumeroSimplesDTO:
    def __init__(self, id: int, value: str, suspect: bool, numeros: list[dict]):
        self.id = id
        self.value = value
        self.suspect = suspect
        self.numeros = numeros or []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "value": self.value,
            "suspect": self.suspect,
            "numeros": self.numeros
        }
