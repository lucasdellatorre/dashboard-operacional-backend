from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero
from collections import defaultdict

class NumeroService():
    def __init__(self, numero_repository: INumeroRepository):
        self.repository = numero_repository
        
    def numeroIsOnOperation(self, numero_id, operacoes_id):
        return self.repository.numeroIsOnOperation(numero_id, operacoes_id)
        
    def find(self, numero_id) -> Numero:
        return self.repository.find(numero_id)
    
    def isAlvo(self, numero_id) -> bool:
        return self.repository.isAlvo(numero_id)
    
    def listarNumeroOperacao(self, operacao_ids: list[int]):
        return self.repository.buscaNumero(operacao_ids)
    
    def listar_numeros(self) -> list[Numero]:
        return self.repository.listar_todos()
