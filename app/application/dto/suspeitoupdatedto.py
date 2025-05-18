from app.domain.entities.suspeito import Suspeito as SuspeitoEntity

class SuspeitoUpdateDTO:
    def __init__(self, nome=None, cpf=None, apelido=None, anotacoes=None, relevante=None, id=None, internalTicketNumber=None):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.nome = nome
        self.cpf = cpf
        self.apelido = apelido
        self.anotacoes = anotacoes
        self.relevante = relevante

    def to_dict(self):
        return {
            'id': self.id,
            'internal_ticket_number': self.internalTicketNumber,
            'nome': self.nome,
            'cpf': self.cpf,
            'apelido': self.apelido,
            'anotacoes': self.anotacoes,
            'relevante': self.relevante
        }

    @staticmethod
    def fromEntity(entity: SuspeitoEntity):
        return SuspeitoUpdateDTO(
            id=entity.id,
            internalTicketNumber=entity.internalTicketNumber,
            nome=entity.nome,
            cpf=entity.cpf,
            apelido=entity.apelido,
            anotacoes=entity.anotacoes,
            relevante=entity.relevante
        )
