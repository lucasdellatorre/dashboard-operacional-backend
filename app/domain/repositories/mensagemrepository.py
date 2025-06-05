from abc import ABC, abstractmethod
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from typing import List, Dict

class IMensagemRepository(ABC):
    @abstractmethod
    def get_mensagens_from_numero_id(self, numero_id) -> list[DomainMensagem]:
        raise (NotImplementedError)

    @abstractmethod
    def get_mensagens_by_ip(self, ip_id: int) -> List[DomainMensagem]:
        raise (NotImplementedError)