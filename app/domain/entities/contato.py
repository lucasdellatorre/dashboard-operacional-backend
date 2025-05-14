class Contato:
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        tipoContato: bool,
        contato: str,
        numeroId: int
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.tipoContato = tipoContato
        self.contato = contato
        self.numeroId = numeroId