from app.domain.entities.numerosuspeito import NumeroSuspeito
from app.domain.entities.suspeitoemail import SuspeitoEmail

class Suspeito:
    def __init__(
        self,
        id: int,
        internalTicketNumber: str,
        nome: str = None,
        cpf: str = None,
        anotacoes: str = None,
        apelido: str = None,
        relevante: bool = None,
        lastUpdateDate: str = None,
        lastUpdateCpf: str = None,
        emails: list[SuspeitoEmail] = None,
        numerosuspeito: list[NumeroSuspeito] = None,
    ):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.nome = nome
        self.cpf = cpf
        self.anotacoes = anotacoes
        self.apelido = apelido
        self.relevante = relevante
        self.lastUpdateDate = lastUpdateDate
        self.lastUpdateCpf = lastUpdateCpf
        self.emails = emails or []
        self.numerosuspeito = numerosuspeito or []
