from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.mensagem import Mensagem

class IMensagemIPRepository(ABC):
    @abstractmethod
    def buscar_mensagens_por_ip(self, filtro: Mensagem) -> List[Mensagem]:
        pass
