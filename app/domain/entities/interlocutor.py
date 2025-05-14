class Interlocutor:
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        numeroId: int,
        descricao: str = None,
        nome: str = None,
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.descricao = descricao
        self.nome = nome
        self.numeroId = numeroId