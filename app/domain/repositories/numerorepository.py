from abc import ABC, abstractmethod
from app.domain.entities.numero import Numero as DomainNumero
from app.application.dto.listanumerodto import ListaNumeroDTO
from typing import List

class INumeroRepository(ABC):
    @abstractmethod
    def find(self, numero_id) -> DomainNumero:
        raise (NotImplementedError)
    
    @abstractmethod
    def isAlvo(self, numero_id) -> bool:
        raise (NotImplementedError)
    
    @abstractmethod
    def buscaNumero(self, operacao_ids: List[int]) -> list[ListaNumeroDTO]:
       raise NotImplementedError()

    @abstractmethod
    def BuscarOperacoesNumero(self) -> list[dict]:
        raise NotImplementedError()
    
    @abstractmethod
    def listar_todos(self) -> list[DomainNumero]:
        """Retorna todos os números presentes na tabela interceptacoes_numeros, com seus respectivos valores."""
        raise NotImplementedError()