from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.numero import Numero as DomainNumero
from app.application.dto.listanumerodto import ListaNumeroDTO

class INumeroRepository(ABC):
    @abstractmethod
    def find(self, numero_id) -> DomainNumero:
        raise NotImplementedError()

    @abstractmethod
    def isNumero(self, numero_id) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def isAlvo(self, numero_id) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def buscaNumero(self, operacao_ids: List[int]) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def BuscarOperacoesNumero(self) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def listar_todos(self) -> list[DomainNumero]:
        """Retorna todos os números presentes na tabela interceptacoes_numeros, com seus respectivos valores."""
        raise NotImplementedError()

    @abstractmethod
    def get_all_by_ids(self, numero_ids: list[int]) -> list[DomainNumero]:
        """Retorna todos os números cujo ID está presente na lista fornecida."""
        raise NotImplementedError()

    @abstractmethod
    def listar_com_suspeitos(self) -> list[dict]:
        """
        Retorna todos os números interceptados com seus respectivos dados de suspeito (se houver).
        Cada item deve conter: id, numero, apelido (ou None), e flag booleana indicando se é suspeito.
        """
        raise NotImplementedError()
