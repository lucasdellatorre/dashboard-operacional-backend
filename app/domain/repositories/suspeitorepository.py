from abc import ABC, abstractmethod
from app.domain.entities.suspeito import Suspeito
from app.domain.entities.suspeitoemail import SuspeitoEmail


class ISuspeitoRepository(ABC):
    @abstractmethod
    def atualizar(self, id: int, dados: dict) -> dict:
        raise (NotImplementedError)

    @abstractmethod
    def get_by_id_with_relations(self, id: int) -> Suspeito | None:
        """Busca um suspeito por ID com todas as relações carregadas."""
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