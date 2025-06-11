from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero
from collections import defaultdict

class NumeroService():
    def __init__(self, numero_repository: INumeroRepository):
        self.repository = numero_repository
        
    def find(self, numero_id) -> Numero:
        return self.repository.find(numero_id)

    def isNumero(self, numero_id) -> bool:
        return self.repository.isNumero(numero_id)
    
    def isAlvo(self, numero_id) -> bool:
        return self.repository.isAlvo(numero_id)
    
    def listarNumeroOperacao(self, operacao_ids: list[int]):
        return self.repository.buscaNumero(operacao_ids)
    
    def listar_numeros(self) -> list[Numero]:
        return self.repository.listar_todos()
    
    def find_all_by_ids(self, ids: list[int]) -> list[Numero]:
     return self.repository.get_all_by_ids(ids)