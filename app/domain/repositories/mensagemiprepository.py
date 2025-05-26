from abc import ABC, abstractmethod
from typing import List
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.domain.entities.mensagem import Mensagem

class IMensagemIPRepository(ABC):
    @abstractmethod
    def buscar_mensagens_por_ip(self, filtro: FiltroMensagemDTO) -> List[Mensagem]:
        pass
