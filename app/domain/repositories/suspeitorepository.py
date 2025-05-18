from abc import ABC, abstractmethod
from app.domain.entities.suspeito import Suspeito

class ISuspeitoRepository(ABC):

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
