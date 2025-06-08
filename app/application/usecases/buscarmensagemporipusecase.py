from typing import List
from app.domain.entities.mensagem import Mensagem
from app.application.dto.mensagemresponsedto import MensagemResponseDTO
from app.domain.services.ipmensagemservice import IpmensagemService
from app.application.dto.filtromensagemdto import FiltroMensagemDTO

class BuscarMensagemPorIPUseCase:
    def __init__(self, ipmensagem_service: IpmensagemService):
        self.mensagem_service = ipmensagem_service

    def execute(self, filtro: FiltroMensagemDTO) -> List[MensagemResponseDTO]:
        mensagens = self.mensagem_service.buscar_mensagens_por_ip(filtro)
        dtos = []
        for numero in filtro.numero:
            ocorrencias = [m for m in mensagens
                           if m.remetente == numero or m.destinatario == numero]
            dtos.append(MensagemResponseDTO.from_ocorrencias(numero, ocorrencias))
        return dtos
