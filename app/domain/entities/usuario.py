class Usuario:
    def __init__(self, cpf: str, id: int | None = None):
        self.id = id
        self.cpf = cpf