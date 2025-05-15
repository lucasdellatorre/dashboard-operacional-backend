from abc import ABC, abstractmethod
from app.domain.entities.numero import Numero as DomainNumero
from app.application.dto.listaoperacaodto import ListaOperacaoDTO
from typing import List

class INumeroRepository(ABC):
    @abstractmethod
    def find(self, numero_id) -> DomainNumero:
        raise (NotImplementedError)
    
    @abstractmethod
    def isAlvo(self, numero_id) -> bool:
        raise (NotImplementedError)
    
    @abstractmethod
    def buscaOperacoes(self, operacao_ids: List[int]) -> list[ListaOperacaoDTO]:
       raise NotImplementedError()

    @abstractmethod
    def BuscarOperacoesNumero(self) -> list[dict]:
        raise NotImplementedError()