from app.domain.entities.suspeito import Suspeito as SuspeitoEntity

class SuspeitoUpdateDTO:
    def __init__(self, nome=None, cpf=None, apelido=None, anotacoes=None, relevante=None, id=None, lastUpdateDate=None, lastUpdateCpf=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.apelido = apelido
        self.anotacoes = anotacoes
        self.relevante = relevante
        self.lastUpdateDate = lastUpdateDate
        self.lastUpdateCpf = lastUpdateCpf

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'apelido': self.apelido,
            'anotacoes': self.anotacoes,
            'relevante': self.relevante,
            'lastUpdateDate': self.lastUpdateDate,
            'lastUpdateCpf': self.lastUpdateCpf
        }

    @staticmethod
    def fromEntity(entity: SuspeitoEntity):
        return SuspeitoUpdateDTO(
            id=entity.id,
            nome=entity.nome,
            cpf=entity.cpf,
            apelido=entity.apelido,
            anotacoes=entity.anotacoes,
            relevante=entity.relevante,
            lastUpdateDate=entity.lastUpdateDate,
            lastUpdateCpf=entity.lastUpdateCpf,
        )
