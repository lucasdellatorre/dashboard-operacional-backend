class CreateSuspeitoDTO:
    def __init__(
        self,
        apelido: str,
        nome: str = "",
        cpf: str = "",
        numeros_ids: list[int] = None,
        lastUpdateCpf: str = ""
    ):
        self.apelido = apelido
        self.nome = nome
        self.cpf = cpf
        self.numeros_ids = numeros_ids or []
        self.lastUpdateCpf = lastUpdateCpf

    def to_dict(self):
        return {
            "apelido": self.apelido,
            "nome": self.nome,
            "cpf": self.cpf,
            "numeros_ids": self.numeros_ids,
            "lastUpdateCpf": self.lastUpdateCpf
        }

    @staticmethod
    def from_dict(data: dict):
        apelido = data.get("apelido")
        numeros = data.get("numeros_ids")

        if not apelido:
            raise ValueError("O campo 'apelido' é obrigatório.")
        if not numeros or not isinstance(numeros, list) or len(numeros) == 0:
            raise ValueError("A lista 'numeros_ids' deve conter ao menos um ID.")

        return CreateSuspeitoDTO(
            apelido=apelido,
            nome=data.get("nome", ""),
            cpf=data.get("cpf", ""),
            numeros_ids=numeros
        )
