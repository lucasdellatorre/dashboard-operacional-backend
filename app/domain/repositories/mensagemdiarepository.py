from abc import ABC, abstractmethod
from typing import List
from app.application.dto.mensagempordiaresponsedto import MensagemPorDiaResponseDTO
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.entities.mensagem import Mensagem

class IMensagemDiaRepository(ABC):
    @abstractmethod
    def buscar_mensagens_por_dia(self, filtro: MensagensRequestDTO, ticket_numbers: List[str]) -> List[MensagemPorDiaResponseDTO]:
        pass
