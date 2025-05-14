from app.domain.entities.operacao import Operacao

class OperacaoDTO:
    def __init__(self, nome: str, id = None):
        self.id = id
        self.nome = nome
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
        
    @staticmethod
    def fromEntity(operacao: Operacao):
        return OperacaoDTO(nome = operacao.nome, id = operacao.id)
    
