from app.domain.repositories.operacaorepository import IOperacaoRepository
from app.domain.entities.operacao import Operacao

class OperacaoService():
    def __init__(self, operacao_repository: IOperacaoRepository):
        self.operacao_repository = operacao_repository
        
    def hasOperacao(self, operacao_id) -> bool:
        return self.operacao_repository.hasOperacao(operacao_id)

    def get_all_operacoes(self):
        return self.operacao_repository.get_all_operations()
    
    def create_operacao(self, nome: str) -> Operacao:
        operacao = Operacao(nome=nome)
        return self.operacao_repository.create(operacao)
    
    def find_by_name(self, nome: str) -> bool:
        return self.operacao_repository.find_by_name(nome)
    
    
        
    

    
    
    
