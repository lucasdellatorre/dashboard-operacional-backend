from abc import ABC, abstractmethod
from app.domain.entities.numero import Numero as DomainNumero

class INumeroRepository(ABC):
    @abstractmethod
    def find(self, numero_id) -> DomainNumero:
        raise (NotImplementedError)
    
    @abstractmethod
    def isAlvo(self, numero_id) -> bool:
        raise (NotImplementedError)