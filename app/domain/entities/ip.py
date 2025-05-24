class IP():
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        ip: str,
        versao: str,
        numeroId: int,
        data: str = None,
        hora: str = None,
        timestamp: str = None
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.ip = ip
        self.versao = versao
        self.numeroId = numeroId
        self.data = data
        self.hora = hora
        self.timestamp = timestamp