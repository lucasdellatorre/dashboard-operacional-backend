from abc import ABC, abstractmethod
from app.domain.entities.operacao import Operacao

class IOperacaoRepository(ABC):
    
    @abstractmethod
    def create(self, operacao: Operacao) -> Operacao:
        raise (NotImplementedError)
    
    def hasOperacao(self, operacao_id) -> bool:
        raise (NotImplementedError)
    
    @abstractmethod
    def get_all_operations(self) -> list[Operacao]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_name(self, nome: str) -> bool:
        raise NotImplementedError
    