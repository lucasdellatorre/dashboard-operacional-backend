from typing import List
from app.application.dto.mensagemresponsedto import MensagemResponseDTO
from app.domain.services.ipmensagemservice import IpmensagemService
from app.application.dto.filtromensagemdto import FiltroMensagemDTO

class BuscarMensagemPorIPUseCase:
    def __init__(self, ipmensagem_service: IpmensagemService):
        self.mensagem_service = ipmensagem_service

    def execute(self, filtro: FiltroMensagemDTO) -> List[MensagemResponseDTO]:
        mensagens = self.mensagem_service.buscar_mensagens_por_ip(filtro)
        return [MensagemResponseDTO(m) for m in mensagens]
