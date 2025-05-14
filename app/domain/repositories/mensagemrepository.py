from abc import ABC, abstractmethod
from app.domain.entities.mensagem import Mensagem as DomainMensagem

class IMensagemRepository(ABC):
    @abstractmethod
    def get_mensagens_from_numero_id(self, numero_id) -> list[DomainMensagem]:
        raise (NotImplementedError)