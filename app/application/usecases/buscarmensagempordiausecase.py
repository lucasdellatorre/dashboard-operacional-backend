from typing import List
from app.domain.entities.mensagem import Mensagem
from app.application.dto.mensagemresponsedto2 import MensagemResponseDTO
from app.domain.services.diamensagemservice import DiamensagemService

class BuscarMensagemPorDiaUseCase:
    def __init__(self, diamensagem_service: DiamensagemService):
        self.mensagem_service = diamensagem_service

    def execute(self, filtro: Mensagem) -> List[MensagemResponseDTO]:
        mensagens = self.mensagem_service.buscar_mensagens_por_dia(filtro)
        return [MensagemResponseDTO(m) for m in mensagens]
