from app.domain.entities.ip import IP

class Numero:
    def __init__(
        self,
        numero: str,
        internalTicketNumber: str,
        id: int | None = None,
        ips: list[IP] = None
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.numero = numero
        self.ips = ips or []
