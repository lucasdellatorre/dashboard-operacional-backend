from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero

class NumeroService():
    def __init__(self, numero_repository: INumeroRepository):
        self.repository = numero_repository
        
    def find(self, numero_id) -> Numero:
        return self.repository.find(numero_id)
    
    def isAlvo(self, numero_id) -> bool:
        return self.repository.isAlvo(numero_id)