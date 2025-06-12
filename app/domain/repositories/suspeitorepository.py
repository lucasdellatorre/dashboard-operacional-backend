from abc import ABC, abstractmethod
from typing import List, Optional

from app.application.dto.filtrodto import FiltroDTO
from app.domain.entities.suspeito import Suspeito
from app.domain.entities.suspeitoemail import SuspeitoEmail


class ISuspeitoRepository(ABC):

    @abstractmethod
    def deletar(self, id: int):
        pass
    
    @abstractmethod
    def atualizar(self, entity: Suspeito):
        pass

    @abstractmethod
    def get_by_id_with_relations(self, id: int) -> Suspeito | None:
        """Busca um suspeito por ID com todas as relações carregadas."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Suspeito | None:
        pass

    @abstractmethod
    def get_numeros_by_suspeito_ids(self, suspeito_ids: list[int]) -> list[str]:
        pass

    @abstractmethod
    def get_by_numero_id_with_relations(self, numero_id: int) -> Suspeito | None:
        """
        Busca o suspeito relacionado a um número (se existir),
        incluindo os números vinculados a esse suspeito.
        """
        pass

    @abstractmethod
    def get_by_apelido(self, apelido: str) -> Suspeito | None:
        """Retorna um suspeito com o apelido exato, se existir."""
        pass

    @abstractmethod
    def create(self, suspeito: Suspeito) -> Suspeito:
        """
        Cria e persiste um novo suspeito.
        Deve retornar o objeto com ID preenchido após a inserção.
        """
        pass
    
    @abstractmethod
    def delete_email(self, suspeito_id, email_id):
        """
        Deleta um email do suspeito.
         Deve retornar um valor booleano expressando o sucesso da operação.
        """
        pass
    
    @abstractmethod
    def create_email(self, suspeito_email: SuspeitoEmail) -> bool:
        """
        Cria e persiste um novo email do suspeito.
        Deve retornar um valor booleano expressando o sucesso da operação.
        """
        pass
    
    @abstractmethod
    def get_all_email(self) -> list[SuspeitoEmail]:
        """
        Retorna todos emails do suspeito.
        """
        pass

    @abstractmethod
    def is_suspeito(self) -> bool:
        raise(NotImplementedError)

    @abstractmethod
    def add_telefone(self, suspeito_id, telefones, cpf) -> bool:
        """
        Adiciona telefones novos para um suspeito
        """
        pass

    @abstractmethod
    def get_email_by_id(self, email_id: int) -> SuspeitoEmail | None:
        """
        Busca um objeto SuspeitoEmail pelo ID.
        """
        pass

    @abstractmethod
    def update_email(self, email: SuspeitoEmail) -> SuspeitoEmail:
        """
        Atualiza um email existente.
        Deve retornar o objeto atualizado.
        """
        pass

    @abstractmethod
    def buscar_por_filtro(
            self,
            numeros: Optional[List[str]],
            suspeitos: Optional[List[str]],
            operacoes: Optional[List[str]],
            grupo: Optional[str],
            tipo: Optional[str],
            data_inicial: Optional[str],
            data_final: Optional[str],
            hora_inicio: Optional[str],
            hora_fim: Optional[str]
    ) -> List[Suspeito]:
        raise NotImplementedError