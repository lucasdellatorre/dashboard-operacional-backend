from app.domain.entities.operacao import Operacao

class OperacaoDTO:
    def __init__(self, nome: str, dataCriacao = None, id = None):
        self.id = id
        self.nome = nome
        self.dataCriacao = dataCriacao
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_criacao': self.dataCriacao
        }
        
    @staticmethod
    def fromEntity(operacao: Operacao):
        return OperacaoDTO(nome = operacao.nome, dataCriacao=operacao.dataCriacao , id = operacao.id)
    