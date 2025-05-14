class Numero:
    def __init__(self, numero: str, internalTicketNumber: str, id: int | None = None):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.numero = numero