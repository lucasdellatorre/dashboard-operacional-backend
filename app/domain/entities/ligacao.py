class Ligacao:
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        criadorLigacao: str = None,
        tipoLigacao: str = None,
        criadorIp: str = None,
        criadorPort: str = None,
        receptor: str = None,
        receptorIp: str = None,
        receptorPort: str = None,
        data: str = None,
        hora: str = None,
        timestamp = None,  # Pode ser datetime.datetime
        numeroId: int = None
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.criadorLigacao = criadorLigacao
        self.tipoLigacao = tipoLigacao
        self.criadorIp = criadorIp
        self.criadorPort = criadorPort
        self.receptor = receptor
        self.receptorIp = receptorIp
        self.receptorPort = receptorPort
        self.data = data
        self.hora = hora
        self.timestamp = timestamp
        self.numeroId = numeroId