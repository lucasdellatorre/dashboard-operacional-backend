from app.domain.entities.suspeito import Suspeito
from app.domain.entities.numerosuspeito import NumeroSuspeito
from app.domain.entities.suspeitoemail import SuspeitoEmail

class SuspeitoDTO:
    def __init__(
        self,
        id: int,
        apelido: str,
        nome: str,
        cpf: str,
        relevante: bool,
        anotacoes: str,
        lastUpdateDate: str,
        lastUpdateCpf: str,
        emails: list[dict],
        numerosuspeito: list[dict]
    ):
        self.id = id
        self.apelido = apelido
        self.nome = nome
        self.cpf = cpf
        self.relevante = relevante
        self.anotacoes = anotacoes
        self.lastUpdateDate = lastUpdateDate
        self.lastUpdateCpf = lastUpdateCpf
        self.emails = emails
        self.numerosuspeito = numerosuspeito

    @staticmethod
    def fromEntity(entity: Suspeito) -> "SuspeitoDTO":
        return SuspeitoDTO(
            id=entity.id,
            apelido=entity.apelido,
            nome=entity.nome,
            cpf=entity.cpf,
            relevante=entity.relevante,
            anotacoes=entity.anotacoes,
            lastUpdateDate=entity.lastUpdateDate,
            lastUpdateCpf=entity.lastUpdateCpf,
            emails=[
                {
                    "id": email.id,
                    "email": email.email,
                    "lastUpdateCpf": email.lastUpdateCpf,
                    "lastUpdateDate": email.lastUpdateDate,
                    "suspeitoId": email.suspeitoId
                }
                for email in entity.emails
            ],
            numerosuspeito=[
                {
                    "numeroId": ns.numero.id,
                    "numero": ns.numero.numero,
                    "lastUpdateCpf": ns.lastUpdateCpf,
                    "lastUpdateDate": ns.lastUpdateDate
                }
                for ns in entity.numerosuspeito
            ]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "apelido": self.apelido,
            "nome": self.nome,
            "cpf": self.cpf,
            "relevante": self.relevante,
            "anotacoes": self.anotacoes,
            "lastUpdateDate": self.lastUpdateDate,
            "lastUpdateCpf": self.lastUpdateCpf,
            "emails": self.emails,
            "numerosuspeito": self.numerosuspeito
        }
