class SuspeitoDetalhadoDTO:
    def __init__(
        self,
        id: int,
        nome: str | None,
        apelido: str | None,
        cpf: str | None,
        relevante: bool | None,
        anotacoes: str | None,
        emails: list[dict],
        celulares: list[dict],
        ips: list[str],
    ):
        self.id = id
        self.nome = nome
        self.apelido = apelido
        self.cpf = cpf
        self.relevante = relevante
        self.anotacoes = anotacoes
        self.emails = emails
        self.celulares = celulares
        self.ips = ips

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "apelido": self.apelido,
            "cpf": self.cpf,
            "relevante": self.relevante,
            "anotacoes": self.anotacoes,
            "emails": self.emails,
            "celulares": self.celulares,
            "ips": self.ips,
        }

    @staticmethod
    def from_entity(entity):
        return SuspeitoDetalhadoDTO(
            id=entity.id,   
            nome=entity.nome,
            apelido=entity.apelido,
            cpf=entity.cpf,
            relevante=entity.relevante,
            anotacoes=entity.anotacoes,
            emails=[
                {
                    "email": email.email,
                    "lastUpdateCpf": email.lastUpdateCpf,
                    "lastUpdateDate": email.lastUpdateDate,
                }
                for email in getattr(entity, 'emails', [])
            ],
            celulares=[
                {
                    "numero": numero_suspeito.numero.numero,
                    "lastUpdateCpf": numero_suspeito.lastUpdateCpf,
                    "lastUpdateDate": numero_suspeito.lastUpdateDate,
                }
                for numero_suspeito in getattr(entity, 'numerosuspeito', [])
            ],
            ips=[
                ip.ip
                for numero_suspeito in getattr(entity, 'numerosuspeito', [])
                for ip in getattr(numero_suspeito.numero, 'ips', [])
            ]
        )
