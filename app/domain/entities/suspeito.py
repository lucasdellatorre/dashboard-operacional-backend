from app.domain.entities.numerosuspeito import NumeroSuspeito
from app.domain.entities.suspeitoemail import SuspeitoEmail

class Suspeito:
    def __init__(
        self,
        id: int = None,
        nome: str = "",
        cpf: str = "",
        anotacoes: str = "",
        apelido: str = "",
        relevante: bool = False,
        lastUpdateDate: str = "",
        lastUpdateCpf: str = "",
        emails: list = None,
        numerosuspeito: list = None
    ):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.anotacoes = anotacoes
        self.apelido = apelido
        self.relevante = relevante
        self.lastUpdateDate = lastUpdateDate
        self.lastUpdateCpf = lastUpdateCpf
        self.emails = emails or []
        self.numerosuspeito = numerosuspeito or []
