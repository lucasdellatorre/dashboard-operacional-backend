class Alvo:
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        numeroId: int,
        nome: str = None,
        cpf: str = None,
        descricao: str = None,
        apelidos: str = None,
        email: str = None
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.nome = nome
        self.cpf = cpf
        self.descricao = descricao
        self.apelidos = apelidos
        self.email = email
        self.numeroId = numeroId