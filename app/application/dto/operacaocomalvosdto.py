from app.domain.entities.operacao import Operacao

class OperacaoComAlvosDTO:
    def __init__(self, nome: str, dataCriacao=None, id=None, qtd_alvos: int = 0):
        self.id = id
        self.nome = nome
        self.dataCriacao = dataCriacao
        self.qtd_alvos = qtd_alvos
        

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_criacao': self.dataCriacao,
            'qtd_alvos': self.qtd_alvos
        }

    @staticmethod
    def fromEntity(operacao: Operacao, qtd_alvos: int = 0):
        return OperacaoComAlvosDTO(
            nome=operacao.nome,
            dataCriacao=operacao.dataCriacao,
            id=operacao.id,
            qtd_alvos=qtd_alvos
        )