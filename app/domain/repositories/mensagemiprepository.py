from abc import ABC, abstractmethod
from typing import List
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.application.dto.mensagemporipresponsedto import MensagemPorIpResponseDTO

class IMensagemIPRepository(ABC):
    @abstractmethod
    def buscar_mensagens_por_ip(self, filtro: FiltroMensagemDTO, tickets: list[str]) -> List[MensagemPorIpResponseDTO]:
        pass
